from odoo import models, fields, api
from odoo.exceptions import ValidationError

class WalletDepositWizard(models.TransientModel):
    _name = 'wallet.deposit.wizard'
    _description = 'Asistente de Depósito Inicial'

    wallet_id = fields.Many2one('wallet.account', string='Billetera', required=True)
    amount = fields.Monetary(string='Monto a Depositar', currency_field='currency_id')
    currency_id = fields.Many2one(related='wallet_id.currency_id')

    def action_apply_deposit(self):
        self.ensure_one()
        if self.amount <= 0:
            raise ValidationError("El monto debe ser mayor a cero.")
            
        # Creamos la transacción directamente confirmada
        self.env['wallet.transaction'].create({
            'wallet_id': self.wallet_id.id,
            'type': 'deposit',
            'amount': self.amount,
            'state': 'confirmed',
            'name': 'Depósito Inicial'
        })
        return {'type': 'ir.actions.act_window_close'}