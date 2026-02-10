from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    gym_member_ids = fields.One2many(
        'gym.member', 
        'partner_id', 
        string="Membresías de Gimnasio"
    )

    is_socio = fields.Boolean(
        string="Es Socio Activo",
        compute="_compute_gym_status",
        store=True
    )
    
    fecha_vencimiento = fields.Date(
        string="Vencimiento de Cuota",
        compute="_compute_gym_status",
        store=True
    )

    @api.depends('gym_member_ids.active_membership', 'gym_member_ids.end_date')
    def _compute_gym_status(self):
        for partner in self:
            active_record = partner.gym_member_ids.filtered(lambda m: m.active_membership)
            
            if active_record:
                latest = max(active_record.mapped('end_date'))
                partner.is_socio = True
                partner.fecha_vencimiento = latest
            else:
                partner.is_socio = False
                partner.fecha_vencimiento = False