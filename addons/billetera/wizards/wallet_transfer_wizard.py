from odoo import models, fields, api
from odoo.exceptions import ValidationError

class WalletTransferWizard(models.TransientModel):
    _name = 'wallet.transfer.wizard'
    _description = 'Asistente de Transferencia'

    from_wallet_id = fields.Many2one('wallet.account', string='Desde', required=True)
    to_wallet_id = fields.Many2one('wallet.account', string='Hacia', required=True)
    amount = fields.Monetary(string='Monto a Enviar', required=True)
    currency_id = fields.Many2one(related='from_wallet_id.currency_id')

    def action_apply_transfer(self):
        self.ensure_one()
        if self.amount <= 0:
            raise ValidationError("El monto debe ser mayor a cero.")
        if self.from_wallet_id.balance < self.amount:
            raise ValidationError("Saldo insuficiente.")
        if self.from_wallet_id == self.to_wallet_id:
            raise ValidationError("No puedes transferirte a ti mismo.")

        # Crear el egreso en la cuenta origen hacia la cuenta destino
        tx = self.env['wallet.transaction'].create({
            'wallet_id': self.from_wallet_id.id,
            'to_wallet_id': self.to_wallet_id.id,
            'type': 'transfer',
            'amount': self.amount,
            'state': 'draft',
        })
        tx.action_confirm()
        return {'type': 'ir.actions.act_window_close'}