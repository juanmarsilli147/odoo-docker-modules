from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Book(models.Model):
    _name = "biblioteca.books"
    _description = "Books"

    name = fields.Char(string="Name", required=True)
    author = fields.Char(string="Author", required=True)
    isbn = fields.Char(string="ISBN")
    is_loaned = fields.Boolean(string="Loaned", default=False)

    

class Loan(models.Model):
    _name = "biblioteca.loan"
    _description = "Loan"

    book_id = fields.Many2one("biblioteca.books", string="Book", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    loan_date = fields.Date(string="Loan Date", default=fields.Date.today())
    return_date = fields.Date(string="Return Date")

    state = fields.Selection([
        ("draft", "Borrador"),
        ("confirmed", "Prestado"),
        ("returned", "Devuelto"),
    ], string="State", default="draft")


    @api.onchange('loan_date')
    def _onchange_loan_date(self):
        if self.loan_date:
            self.return_date = self.loan_date + timedelta(days=15)


    @api.constrains('book_id')
    def _check_book_availability(self):
        for record in self:
            if record.book_id.is_loaned:
                raise ValidationError("¡Este libro ya se encuentra prestado!")


    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'
            record.book_id.is_loaned = True

    def action_return(self):
        for record in self:
            record.state = 'returned'
            record.book_id.is_loaned = False
    
    