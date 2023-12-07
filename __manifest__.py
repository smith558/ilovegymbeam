# -*- coding: utf-8 -*-
{
    'name': "I love GymBeam",
    'application': True,
    'category': 'Human Resources',
    'auto_install': False,
    'icon': '/ilovegymbeam/static/assets/gb-icon.png',
    'version': '1.0',
    'depends': ['base', 'hr', 'hr_recruitment', 'website_hr_recruitment'],
    'author': "Stanislav Modrak",
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'views/employee_view.xml',
        'views/applicant_view.xml',
        'views/job_view.xml',
        'views/templates.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'ilovegymbeam/static/js/**/*',
            'ilovegymbeam/static/css/**/*',
        ]
    },
}
