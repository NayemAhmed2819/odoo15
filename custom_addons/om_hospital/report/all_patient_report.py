from odoo import api, fields, models

class AllPatientReport(models.AbstractModel):
    _name = 'report.om_hospital.report_all_patient_list'
    _description = 'Patient Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = []
        gender = data.get('form').get('gender')
        age = data.get('form').get('age')
        if gender:
            domain += [('gender', '=', gender)]
        if age != 0:
            domain += [('age', '=', age)]
        docs = self.env['hospital.patient'].search(domain)
        return {
            'docs': docs,
        }