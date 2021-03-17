{
    'name': 'School Management System',
    'summary': """This module will add a record to store student  and teacher details""",
    'version': '10.0.1.0.0',
    'description': """This module will add a record to store student and teacher details""",
    'author': 'Nirmla Shrimali',
    'company': 'Brainvire Info Tech',
    'website': 'https://www.brainvireinfotech.com',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
       
        'security/ir.model.access.csv',
        'data/ir.sequence.student.xml',
        'data/ir.sequence.teacher.xml',
        'views/student_views.xml',
        'views/recruitment_views.xml',
        'views/document_views.xml',
        'views/standard_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}