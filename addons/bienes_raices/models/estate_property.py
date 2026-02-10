from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    _order = "id desc"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection([
        ('new', 'Nuevo'),
        ('offer_received', 'Oferta Recibida'),
        ('offer_accepted', 'Oferta Aceptada'),
        ('sold', 'Vendido'),
        ('canceled', 'Cancelado'),
    ], string="Estado", default='new')
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Tipo de Propiedad")
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string="Tags")
    bedrooms = fields.Integer(string="Habitaciones", default=2)
    living_area = fields.Integer(string="Área de Living")
    facades = fields.Integer(string="Facades")
    garden_area = fields.Integer(string="Área de Jardín")
    post_code = fields.Char(string="Código Postal")
    garden_orientation = fields.Selection([
        ('north', 'Norte'),
        ('south', 'Sur'),
        ('east', 'Este'),
        ('west', 'Oeste'),
    ], string="Orientación del Jardín", default='north')
    total_area = fields.Integer(string="Área Total", compute='_compute_total_area')
    date_availability = fields.Date(string="Disponibilidad", default = lambda self: fields.Date.add(fields.Date.today(), months=3), copy=False)
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Jardín", default=False)
    expected_price = fields.Float(string="Precio Esperado", required=True)
    selling_price = fields.Float(string="Precio de Venta", readonly=True, copy=False)
    buyer_id = fields.Many2one(comodel_name='res.partner', string="Comprador")
    salesperson_id = fields.Many2one(comodel_name='res.users', string="Vendedor")
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string="Ofertas")
    best_offer = fields.Float(string="Mejor Oferta", compute='_compute_best_offer')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'El nombre de la propiedad debe ser único'),
        ('check_expected_price', 'check(expected_price > 0)', 'El precio debe ser mayor a 0'),
        ('check_selling_price', 'check(selling_price >= 0)', 'El precio de venta debe ser mayor a 0'),
    ]

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

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            limit_price = record.expected_price * 0.90
            if float_compare(record.selling_price, limit_price, precision_digits=2) == -1:
                raise ValidationError(
                    f"El precio de venta ({record.selling_price}) debe ser al menos el 90% "
                    f"del precio esperado ({record.expected_price})."
                )

    

    
    
    
    


    
