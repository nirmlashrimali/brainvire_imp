{
    'name': 'Brainvire Infotech',
    'summary': """This module will add a record to store employee details""",
    'version': '10.0.1.0.0',
    'description': """This module will add a record to store employee details""",
    'author': 'Nirmla Shrimali',
    'company': 'Brainvire Info Tech',
    'website': 'https://www.brainvireinfotech.com',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
       'security/ir.model.access.csv',
       'views/department_views.xml',
       'views/employee_views.xml',
       'views/admin.xml',

      ],
        'demo': [],
    'installable': True,
    'auto_install': False,
}