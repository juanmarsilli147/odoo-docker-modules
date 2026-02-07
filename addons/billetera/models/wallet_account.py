from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class WalletAccount(models.Model):
    # Caracteristicas del modelo
    _name = 'wallet.account'
    _description = 'Billetera Virtual'
    _rec_name = 'partner_id'

    # Campos del modelo
    partner_id = fields.Many2one(
        'res.partner', 
        string='Titular', 
        required=True, 
        ondelete='restrict'
    )
    currency_id = fields.Many2one(
        'res.currency', 
        string='Moneda', 
        default=lambda self: self.env.company.currency_id
    )
    balance = fields.Monetary(
        string='Saldo Disponible', 
        compute='_compute_balance', 
        store=True, 
        currency_field='currency_id'
    )
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activo')
    ], string='Estado', default='draft')

    transaction_ids = fields.One2many(
        'wallet.transaction', 
        'wallet_id', 
        string='Movimientos'
    )

    _sql_constraints = [
        ('partner_unique', 'unique(partner_id)', '¡Este contacto ya posee una billetera!')
    ]

    @api.depends('transaction_ids.state', 'transaction_ids.amount', 'transaction_ids.type')
    def _compute_balance(self):
        for record in self:
            # Sumamos depósitos y restamos transferencias/retiros
            total = 0.0
            for tx in record.transaction_ids.filtered(lambda x: x.state == 'confirmed'):
                if tx.type == 'deposit':
                    total += tx.amount
                elif tx.type == 'transfer':
                    total -= tx.amount
            record.balance = total

    def action_activate(self):
        self.state = 'active'