from odoo import api, fields, models


class PatientReportWizard(models.TransientModel):
    _name = "patient.report.wizard"
    _description = "Print Patient Wizard"

    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    age = fields.Integer(string="Age")

    def action_print_report(self):
        data = {
            'form': self.read()[0],
        }
        return self.env.ref('om_hospital.action_report_all_patient_details').report_action(self, data=data)

