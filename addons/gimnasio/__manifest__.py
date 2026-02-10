# -*- coding: utf-8 -*-
{
    'name': "Gimnasio",

    'summary': "Modulo de Gestion de Membresia de Gimnasio",

    'description': """
        Modulo de Gestion de Membresia de Gimnasio
    """,

    'author': "Juan Marsilli",
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/gym_member_views.xml',
        'views/partner_gym_inherit_views.xml',
        'views/menus.xml',
    ],

    'application': True,
}

