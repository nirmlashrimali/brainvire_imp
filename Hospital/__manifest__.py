# -*- coding: utf-8 -*-
{
    'name': 'Hospital',
    'summary': """This module will add a record to store doctor and patient details""",
    'version': '10.0.1.0.0',
    'description': """This module will add a record to store doctor and patient details""",
    'author': 'Nirmla Shrimali',
    'company': 'Civil Hospital',
    'website': 'https://www.civilhospital.com',
    'category': 'Tools',
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/doctor.xml',
        'views/patient.xml',
        'views/tablet.xml',
        'views/line.xml',
        'views/sale_order_views.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}