from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner' # Herencia

    is_socio = fields.Boolean(string="Es Socio del Gimnasio")
    nro_socio = fields.Char(string="Número de Socio")
    fecha_vencimiento = fields.Date(string="Vencimiento de Cuota")