# -*- coding: utf-8 -*-
{
    'name': 'Product Image',
    'summary': """This module will add a record to sale product image""",
    'version': '10.0.1.0.0',
    'description': """This module will add a record to sale product image""",
    'author': 'Nirmla Shrimali',
    'company': 'Brainvire Infotech',
    'website': 'https://www.brainvireinfotech.com',
    'category': 'Tools',
    'depends': ['base', 'sale', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_image_inherit_views.xml',
        'report/report_sale_order_image_inherit.xml',
        
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
