# -*- coding: utf-8 -*-
{
    'name': "Gimnasio",

    'summary': "Modulo de Gestion de Membresia de Gimnasio",

    'description': """
        Modulo de Gestion de Membresia de Gimnasio
    """,

    'author': "Juan Marsilli",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/gym_member_views.xml',
    ],

    'application': True,
}

