from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    use_wallet = fields.Boolean(
        string="Pagar con Billetera",
        help="Si se marca, al confirmar la venta se descontará el saldo de la billetera del cliente."
    )

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            if order.use_wallet:
                wallet = self.env['wallet.account'].search([
                    ('partner_id', '=', order.partner_id.id),
                    ('state', '=', 'active')
                ], limit=1)

                if not wallet:
                    raise UserError(_("El cliente no tiene una billetera activa."))

                if wallet.balance < order.amount_total:
                    raise UserError(_("Saldo insuficiente en la billetera del cliente (Saldo: %s).") % wallet.balance)

                self.env['wallet.transaction'].create({
                    'wallet_id': wallet.id,
                    'type': 'transfer',
                    'amount': order.amount_total,
                    'state': 'confirmed',
                    'name': _("Pago de Pedido: %s") % order.name,
                })
        
        return res

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['use_wallet'] = self.use_wallet
        return res