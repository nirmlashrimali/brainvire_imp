# -*- coding: utf-8 -*-
{
    'name': 'Hotel Management',
    'summary': """This module will add a record to store room and customer details""",
    'version': '10.0.1.0.0',
    'description': """This module will add a record to store room and customer details""",
    'author': 'Nirmla Shrimali',
    'company': 'Taj Hotel',
    'website': 'https://www.tajhotel.com',
    'category': 'Tools',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/register_cron_data.xml',
        'report/report_register.xml',
        'report/report_register_templates.xml',
        'data/ir.sequence.room.xml',
        'data/ir.sequence.registration.xml',
        'views/hotel_room_views.xml',
        'views/hotel_registration_views.xml',
        'views/register_document_views.xml',
        'views/customer_guest_views.xml',
        'views/hotel_room_type_views.xml',
        'views/hotel_inquiry_views.xml',
        'views/room_guest_line_views.xml',

        
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}