from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id', string="Properties")

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'El nombre del tipo de propiedad debe ser único'),
    ]
    