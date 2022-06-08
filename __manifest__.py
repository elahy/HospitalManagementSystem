# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Hospital',
    'author': 'Qudrat-E-Elahy',
    'sequence': -100,
    'summary': 'Hospital Management System',
    'description': """Hospital Management System""",
    'depends': ['mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'wizard/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},
    'post_init_hook': '',
    'license': 'LGPL-3',
}
