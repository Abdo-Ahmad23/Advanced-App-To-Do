# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'advanced_to_do_app',
    'version' : '1.0',
    'summary': 'Keep Your Projects & Tasks',
    'sequence': 10,
    'description': "",
    'category': '',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends' : ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_view.xml',
        'views/employee_view.xml',
        'views/task_view.xml',
        'views/project_view.xml',
        'views/manager_view.xml',
    ],
    'images': ['static/description/icon.png'],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
