from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    use_wallet = fields.Boolean(string="Pagado con Billetera", readonly=True, copy=False)

    def action_post(self):
        res = super(AccountMove, self).action_post()

        for move in self:
            if move.use_wallet and move.move_type == 'out_invoice':
                sale_order = self.env['sale.order'].search([('name', '=', move.invoice_origin)], limit=1)
                
                if sale_order:
                    move.message_post(body="Factura pagada automáticamente mediante saldo de Billetera Virtual.")
        return res