# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'To_Do_App',
    'version' : '1.0',
    'summary': 'Invoices & Payments',
    'sequence': 10,
    'description': "",
    'category': '',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends' : ['base_setup', ],
    'data': [
        'views/base_view.xml',
        'views/employee_view.xml',
        'views/task_view.xml',
        'views/project_view.xml',
        'views/manager_view.xml',
        
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
