from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Gym Member'
    
    name = fields.Char(string='Nombre', required=True)
    dni = fields.Char(string='DNI', required=True)
    email = fields.Char(string='Email')
    plan_id = fields.Many2one('gym.plan', string='Plan', required=True)
    
    start_date = fields.Date(string='Fecha de inicio', required=True, default=fields.Date.today)
    end_date = fields.Date(string='Fecha de fin', compute='_compute_end_date', store=True, readonly=False)
    
    active_membership = fields.Boolean(string='Miembro Activo', compute='_compute_active_membership')

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

    def action_renew_membership(self):
        for record in self:
            current_end = record.end_date or fields.Date.today()
            record.end_date = current_end + timedelta(days=30)

class GymPlan(models.Model):
    _name = 'gym.plan'
    _description = 'Gym Plan'
    
    name = fields.Char(string='Nombre', required=True)
    duration_days = fields.Integer(string='Duración en días', required=True, default=30)
    
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    price = fields.Monetary(string='Precio', currency_field='currency_id', required=True)
    