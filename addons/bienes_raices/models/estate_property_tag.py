from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'El nombre de la etiqueta debe ser único'),
    ]