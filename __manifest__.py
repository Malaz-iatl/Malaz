# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'HR Team',
    'version': '1.1',
    'summary': 'hr_team_help_desk ',
    'author': '',
    'category': '',
    'description': "Help Desl",
    'depends': ['mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/group_security.xml',
        'data/ir_sequence.xml',
        'views/hd_team_view.xml',
        'views/hd_ticket_view.xml',
        'wizard/tickets_team_view.xml',
        'report/ticket_team_view.xml',
        'wizard/tickets_team_excel_view.xml'
        

    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
