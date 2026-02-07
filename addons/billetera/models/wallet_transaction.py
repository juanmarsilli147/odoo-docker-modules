from odoo import models, fields, api
from odoo.exceptions import ValidationError

class WalletTransaction(models.Model):
    # Caracteristicas del modelo
    _name = 'wallet.transaction'
    _description = 'Transacción de Billetera'
    _order = 'date desc'
    

    # Campos del modelo
    name = fields.Char(string='Referencia', readonly=True, default='/')
    wallet_id = fields.Many2one('wallet.account', string='Billetera', required=True)
    date = fields.Datetime(string='Fecha', default=fields.Datetime.now)
    
    type = fields.Selection([
        ('deposit', 'Depósito'),
        ('transfer', 'Transferencia')
    ], string='Tipo', required=True)
    
    amount = fields.Monetary(string='Monto', required=True, currency_field='currency_id')
    currency_id = fields.Many2one(related='wallet_id.currency_id')
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='draft')

    # ¿A quién le mandamos el dinero?
    to_wallet_id = fields.Many2one('wallet.account', string='Billetera Destino')

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('wallet.transaction') or 'TX-001'
        return super(WalletTransaction, self).create(vals)

    def action_confirm(self):
        for rec in self:
            # Validación No gastar lo que no se tiene
            if rec.type == 'transfer' and rec.wallet_id.balance < rec.amount:
                raise ValidationError(_("Saldo insuficiente para realizar esta operación."))
            
            # Lógica de transferencia espejo
            if rec.type == 'transfer' and rec.to_wallet_id:
                # Creamos el ingreso en la cuenta destino de forma automática
                self.create({
                    'wallet_id': rec.to_wallet_id.id,
                    'type': 'deposit',
                    'amount': rec.amount,
                    'state': 'confirmed',
                    'name': f"REC: {rec.name}"
                })
            
            rec.state = 'confirmed'