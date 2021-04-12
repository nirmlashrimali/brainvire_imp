{
    'name': 'Doctor Appointment',
    'summary': """This module will add a record to doctor appointment""",
    'version': '10.0.1.0.0',
    'description': """This module will add a record to store appointment""",
    'author': 'Nirmla Shrimali',
    'company': 'Brainvire Info Tech',
    'website': 'https://www.brainvireinfotech.com',
    'category': 'Tools',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/doctor_appointment_views.xml',
        'views/website_inherit_appointment.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
