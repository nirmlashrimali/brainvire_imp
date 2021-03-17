{
    'name': 'School Management',
    'summary': """This module will add a record to store student details""",
    'version': '10.0.1.0.0',
    'description': """This module will add a record to store student details""",
    'author': 'Nirmla Shrimali',
    'company': 'Brainvire Info Tech',
    'website': 'https://www.brainvireinfotech.com',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'views/student_views.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}