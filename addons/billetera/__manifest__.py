# -*- coding: utf-8 -*-
{
    'name': "Billetera",

    'summary': "Modulo de Billetera",

    'description': """
        Modulo de Billetera
    """,

    'author': "Juan Marsilli",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'mail', 'sale', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/wizard_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/wallet_account_views.xml',
        'views/menus.xml',
        'data/ir_sequence_data.xml',
    ],

    'application': True,    
}

