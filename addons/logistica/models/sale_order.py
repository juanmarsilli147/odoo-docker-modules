from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    shipment_count = fields.Integer(compute='_compute_shipment_count')

    def _compute_shipment_count(self):
        for order in self:
            order.shipment_count = self.env['logistics.shipment'].search_count([
                ('sale_id', '=', order.id)
            ])

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        
        for order in self:
            self.env['logistics.shipment'].create({
                'sale_id': order.id,
                'state': 'draft',
                'partner_id': order.partner_id.id, 
            })
        return res

    def action_view_shipments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Envíos Relacionados',
            'res_model': 'logistics.shipment',
            'view_mode': 'list,form',
            'domain': [('sale_id', '=', self.id)],
            'context': {'default_sale_id': self.id},
        }