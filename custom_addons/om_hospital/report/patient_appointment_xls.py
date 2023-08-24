
from odoo import models


class PatientAppointmentXls(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_appointment_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):

        sheet = workbook.add_worksheet('Appointments')
        bold = workbook.add_format({'bold': True})

        sheet.set_column('D:D', 10)
        sheet.set_column('E:E', 18)

        row = 3
        col = 3

        sheet.write(row, col, 'Reference', bold)
        sheet.write(row, col+1, 'Patient Name', bold)
        for appointment in data['appointments']:
            row += 1
            sheet.write(row, col, appointment['seq'])
            sheet.write(row, col + 1, appointment['patient_id'][1])
