from odoo import models, fields, api


class GymPlan(models.Model):
    _name = 'gym.plan'
    _description = 'Plan de Gimnasio'
    
    name = fields.Char(string='Nombre del Plan', required=True)
    duration_days = fields.Integer(string='Duración en días', required=True, default=30)
    
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    price = fields.Monetary(string='Precio', currency_field='currency_id', required=True)