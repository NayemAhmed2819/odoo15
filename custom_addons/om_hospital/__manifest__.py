# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hospital Management',
    'version': '1.1.0',
    'category': 'Hospital',
    'author': 'Nayeem',
    'sequence': -100,
    'summary': 'Hospital Management System',
    'description': """Hospital Management System""",
    'depends': ['mail', 'product', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'data/mail_template_data.xml',
        'wizard/cancel_appointment_view.xml',
        'wizard/appointment_report_view.xml',
        'wizard/all_patient_report_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag_view.xml',
        'views/res_config_settings_views.xml',
        'views/operation_view.xml',
        'views/playground_view.xml',
        'report/patient_card.xml',
        'report/appointment_details.xml',
        'report/pharmacy_details.xml',
        'report/appointment_report_wizard.xml',
        'report/all_patient_report_wizard.xml',
        'report/report.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}