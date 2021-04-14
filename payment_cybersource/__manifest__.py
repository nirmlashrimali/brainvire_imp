# -*- coding: utf-8 -*-
{
    'name': 'Payment Cyber Source',
    'summary': """This module will add a record to payment of product """,
    'version': '10.0.1.0.0',
    'description': """This module will add a record to payment of product """,
    'author': 'Nirmla Shrimali',
    'company': 'Brainvire Infotech',
    'website': 'https://www.brainvireinfotech.com',
    'category': 'Tools',
    'depends': ['base', 'payment_authorize'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_cyber_views.xml',
        'views/payment_cyber_template_views.xml',
        'data/payment_cybersource_data.xml',
        
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
