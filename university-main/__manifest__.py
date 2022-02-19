# -*- coding: utf-8 -*-
{
    'name': "university",

    'summary': """
    Simple odoo module for university management""",

    'description': """
        Develop a new odoo module from scratch which will be concerned as an exam.
        The present module is built for an important purpose which is to ease the whole university process.
    """,

    'author': "Bouchaib MASSIOUI",
    'website': "https://www.linkedin.com/in/bouchaib-massioui/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project Management',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # add access right values
        'security/ir.model.access.csv',
        'views/classroom_views.xml',
        'views/department_views.xml',
        'views/professor_views.xml',
        'views/student_views.xml',
        'views/subject_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}