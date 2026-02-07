from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    currency_id = fields.Many2one('res.currency', compute='_compute_currency_id')

    wallet_balance = fields.Monetary(
        string='Saldo Billetera', 
        compute='_compute_wallet_balance',
        currency_field='currency_id'
    )

    def _compute_currency_id(self):
        for partner in self:
            partner.currency_id = partner.company_id.currency_id or self.env.company.currency_id

    @api.depends('name')
    def _compute_wallet_balance(self):
        for partner in self:
            wallet = self.env['wallet.account'].search([
                ('partner_id', '=', partner.id)
            ], limit=1)
            partner.wallet_balance = wallet.balance if wallet else 0.0

    def action_view_wallet_history(self):
        self.ensure_one()
        wallet = self.env['wallet.account'].search([('partner_id', '=', self.id)], limit=1)
        
        return {
            'name': 'Movimientos de Billetera',
            'type': 'ir.actions.act_window',
            'res_model': 'wallet.transaction',
            'view_mode': 'list,form',
            'domain': [('wallet_id.partner_id', '=', self.id)],
            'context': {'default_wallet_id': wallet.id if wallet else False},
        }