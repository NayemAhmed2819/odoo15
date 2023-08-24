import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta

class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        return res

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        cancel_days = self.env['ir.config_parameter'].get_param('om_hospital.cancel_days')
        allowed_date = self.appointment_id.appointment_date - relativedelta.relativedelta(days=int(cancel_days))
        if allowed_date < date.today():
            raise ValidationError(_("Sorry, cancellation is not allowed on this day!"))
        self.appointment_id.state = 'cancel'

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'cancel.appointment.wizard',
            'target': 'new',
            'res_id': self.id
        }

        # return {
        #     'type': "ir.actions.client",
        #     'tag': 'reload',
        # }
