from odoo import models, fields


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
    date_availability = fields.Date(string="Date Availability", default = lambda self: fields.Date.add(fields.Date.today(), months=3), copy=False)
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    
    
    
    


    
