# -*- coding: utf-8 -*-
{
    'name': 'Global Discount',
    'summary': """This module will add a record to sale order and product details""",
    'version': '10.0.1.0.0',
    'description': """This module will add a record to sale order and product details""",
    'author': 'Nirmla Shrimali',
    'company': 'Brainvire Infotech',
    'website': 'https://www.brainvireinfotech.com',
    'category': 'Tools',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_extend_inherit_views.xml',
        'report/report_sale_order_discount_inherit.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}