# -*- coding: utf-8 -*-
{
    'name': 'Sale Signature',
    'summary': """This module will add a record to sale quotation,delivery and invoice""",
    'version': '10.0.1.0.0',
    'description': """This module will add a record to sale quotation,delivery and invoice""",
    'author': 'Nirmla Shrimali',
    'company': 'Brainvire Infotech',
    'website': 'https://www.brainvireinfotech.com',
    'category': 'Tools',
    'depends': ['base', 'sale', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_signature_inherit_views.xml',
        
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
