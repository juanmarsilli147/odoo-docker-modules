from odoo import http
from odoo.http import request

class ShipmentController(http.Controller):
 
    @http.route('/tracking/<path:shipment_name>', auth='public', website=True)
    def shipment_tracking(self, shipment_name, **kwargs):

        shipment = request.env['logistics.shipment'].sudo().search([
            ('name', '=', shipment_name)
        ], limit=1)
        
        if not shipment:
            return request.render('website.404')
            
        return request.render('logistica.tracking_page_template', {
            'shipment': shipment,
        })

    @http.route('/test_logistica', auth='public', website=True)
    def test_logistica(self, **kwargs):
        return "<h1>El controlador funciona correctamente</h1>"