from odoo import api, models, fields
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string="State", default='new')
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Property Type")
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string="Property Tags", widget="many2many_tags")
    bedrooms = fields.Integer(string="Bed Rooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garden_area = fields.Integer(string="Garden Area")
    post_code = fields.Char(string="Post Code")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string="Garden Orientation", default='north')
    total_area = fields.Integer(string="Total Area", compute='_compute_total_area')
    date_availability = fields.Date(string="Date Availability", default = lambda self: fields.Date.add(fields.Date.today(), months=3), copy=False)
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    buyer_id = fields.Many2one(comodel_name='res.partner', string="Buyer")
    salesperson_id = fields.Many2one(comodel_name='res.users', string="Salesperson")
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string="Offers")
    best_offer = fields.Float(string="Best Offer", compute='_compute_best_offer')

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped('price'), default=0)


    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = self.garden and 10
        self.garden_orientation = self.garden and 'north'

    def action_sold(self):
        if self.filtered(lambda p: p.state == 'canceled'):
            raise UserError("La propiedad cancelada no puede ser vendida")
        self.filtered(lambda p: p.state != 'sold').write({'state': 'sold'})
        return True

    def action_cancel(self):
        if self.filtered(lambda p: p.state == 'sold'):
            raise UserError("La propiedad vendida no puede ser cancelada")
        self.filtered(lambda p: p.state != 'canceled').write({'state': 'canceled'})
        return True

    
    
    
    


    
