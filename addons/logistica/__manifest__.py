{
    'name': "Logistica",

    'summary': "Aplicacion para gestionar logistica de pedidos",

    'description': """
        Aplicacion para gestionar logistica de pedidos
    """,

    'author': "Juan Marsilli",
    'version': '0.1',
    'depends': ['base', 'sale_management', 'stock', 'fleet', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'wizard/assign_driver_views.xml',
        'report/shipment_report.xml',
        'views/logistic_shipment_views.xml',
        'views/sale_order_inherit_views.xml',
        'views/template_web.xml',
    ],

    'application': True,
}
