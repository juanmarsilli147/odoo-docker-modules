from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    bedrooms = fields.Integer(string="Camas")
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garden_area = fields.Integer(string="Garden Area")
    post_code = fields.Char(string="Post Code")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string="Garden Orientation")
    date_availability = fields.Date(string="Date Availability")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    
    
    
    


    
