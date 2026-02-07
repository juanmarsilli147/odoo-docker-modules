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

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/wizard_views.xml',
        'views/wallet_account_views.xml',
        'views/menus.xml',
        'data/ir_sequence_data.xml',
    ],
}

