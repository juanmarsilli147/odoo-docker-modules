from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LogisticsShipment(models.Model):
    _name = 'logistics.shipment'
    _description = 'Envío de Logística'
    _order = 'name desc'

    name = fields.Char(
        string='Referencia de Envío', 
        required=True, copy=False, readonly=True, 
        index=True, default=lambda self: _('Nuevo')
    )
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('ready', 'Listo para Despacho'),
        ('in_transit', 'En Tránsito'),
        ('delivered', 'Entregado'),
        ('cancel', 'Cancelado'),
    ], string='Estado', default='draft')

    sale_id = fields.Many2one('sale.order', string='Orden de Venta', required=True)
    partner_id = fields.Many2one(related='sale_id.partner_id', string='Cliente', store=True)
    
    driver_id = fields.Many2one('res.users', string='Chofer')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehículo')

    total_weight = fields.Float(string='Peso Total (kg)', compute='_compute_total_weight', store=True)

    @api.depends('sale_id.order_line.product_id', 'sale_id.order_line.product_uom_qty')
    def _compute_total_weight(self):
        for record in self:
            weight = 0.0
            if record.sale_id:
                for line in record.sale_id.order_line:
                    weight += line.product_id.weight * line.product_uom_qty
            record.total_weight = weight

    @api.model
    def create(self, vals):
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code('logistics.shipment.seq') or _('Nuevo')
        return super(LogisticsShipment, self).create(vals)

    def action_confirm(self):
        self.write({'state': 'ready'})


    def action_in_transit(self):
        self.write({'state': 'in_transit'})

    def action_delivered(self):
        self.write({'state': 'delivered'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    
    _sql_constraints = [
        ('name_unique', 'unique(name)', '¡La referencia de envío debe ser única!'),
    ]