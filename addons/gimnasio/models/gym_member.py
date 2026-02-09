from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Miembro de Gimnasio'
    _rec_name = 'partner_id'
    
    partner_id = fields.Many2one(
        'res.partner', 
        string='Socio', 
        required=True, 
        ondelete='restrict'
    )

    dni = fields.Char(related='partner_id.vat', string='DNI', readonly=False)
    email = fields.Char(related='partner_id.email', readonly=True)
    
    plan_id = fields.Many2one('gym.plan', string='Plan', required=True)
    
    start_date = fields.Date(string='Fecha de inicio', required=True, default=fields.Date.today)
    end_date = fields.Date(string='Fecha de fin', compute='_compute_end_date', store=True, readonly=False)
    
    active_membership = fields.Boolean(string='Miembro Activo', compute='_compute_active_membership', store=True)

    @api.depends('start_date', 'plan_id.duration_days')
    def _compute_end_date(self):
        for record in self:
            if record.start_date and record.plan_id.duration_days:
                record.end_date = record.start_date + timedelta(days=record.plan_id.duration_days)
            else:
                record.end_date = False

    @api.depends('end_date')
    def _compute_active_membership(self):
        today = fields.Date.today()
        for record in self:
            record.active_membership = record.end_date and record.end_date >= today

    @api.constrains('dni')
    def _check_dni(self):
        for record in self:
            if record.dni:
                if not record.dni.isdigit():
                    raise ValidationError(_("El DNI debe contener solo números."))
                
            
                if self.search_count([('dni', '=', record.dni), ('id', '!=', record.id)]):
                    raise ValidationError(_("El DNI ya se encuentra registrado."))

    @api.constrains('partner_id')
    def _check_unique_member(self):
        for record in self:
            exists = self.search_count([
                ('partner_id', '=', record.partner_id.id), 
                ('id', '!=', record.id)
            ])
            if exists:
                raise ValidationError(_("Este contacto ya está registrado como socio del gimnasio."))

    def action_renew_membership(self):
        self.ensure_one()
        current_end = self.end_date if self.end_date and self.end_date > fields.Date.today() else fields.Date.today()
        self.end_date = current_end + timedelta(days=self.plan_id.duration_days)
