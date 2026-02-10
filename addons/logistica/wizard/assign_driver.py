from odoo import models, fields, api

class AssignDriverWizard(models.TransientModel):
    _name = 'assign.driver.wizard'
    _description = 'Asistente para Asignar Chofer'

    driver_id = fields.Many2one('res.users', string='Chofer', required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehículo', required=True)

    def action_assign(self):
        # Obtenemos los IDs de los registros seleccionados en la vista lista
        active_ids = self.env.context.get('active_ids')
        shipments = self.env['logistics.shipment'].browse(active_ids)
        
        # Actualizamos todos los envíos de una sola vez
        shipments.write({
            'driver_id': self.driver_id.id,
            'vehicle_id': self.vehicle_id.id,
            'state': 'ready'
        })
        return {'type': 'ir.actions.act_window_close'}