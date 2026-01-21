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
        store=True, # Lo guardamos en DB para poder filtrar y ordenar por saldo
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