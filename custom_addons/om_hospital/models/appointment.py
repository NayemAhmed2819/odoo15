# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = "mail.thread", "mail.activity.mixin"
    _description = "Hospital Appointment"
    _rec_name = 'seq'
    _order = 'id desc'

    patient_id = fields.Many2one('hospital.patient', string="Patient", tracking=True, ondelete='cascade')
    ref = fields.Char(string='Reference', tracking=True, related='patient_id.ref')  # related='patient_id.ref'
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', related='patient_id.gender',
                              readonly=False)
    appointment_date = fields.Date(string="Appointment Date", tracking=True)
    booking_time = fields.Datetime(string="Booking Time", default=fields.Datetime.now, readonly=True)
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Drafted'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string="Status", default='draft', required=True, tracking=True)
    doctor_id = fields.Many2one('res.users', string="Doctor", tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string="Hide Sales Price")
    seq = fields.Char(string='Sequence', tracking=True)
    operation = fields.Many2one('hospital.operation', string="Operation")
    progress = fields.Integer(string="Progress", compute='compute_progress')
    duration = fields.Float(string="Duration", tracking=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    total_amount = fields.Monetary(string='Total Amount', compute='_compute_total_amount')

    @api.depends('pharmacy_line_ids.price_subtotal')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.pharmacy_line_ids.mapped('price_subtotal'))

    def compute_amount_total(self):
        for rec in self:
            print(rec.pharmacy_line_ids)

    def unlink(self):
        for rec in self:
            if self.state != 'draft':
                raise ValidationError(_("You can only delete appointments with draft status"))
        return super(HospitalAppointment, self).unlink()

    @api.model
    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        res = super(HospitalAppointment, self).create(vals)
        sl_no = 0
        for line in res.pharmacy_line_ids:
            sl_no += 1
            line.sl_no = sl_no
        return res

    def write(self, vals):
        if not self.seq and not vals.get('seq'):
            vals['seq'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        res = super(HospitalAppointment, self).write(vals)
        sl_no = 0
        for line in self.pharmacy_line_ids:
            sl_no += 1
            line.sl_no = sl_no
        return res

    # To get the reference, we can either use this function or the related syntax
    # @api.onchange('patient_id')
    # def onchange_patient_id(self):
    #     self.ref = self.patient_id.ref('om_hospital.action_hospital_patient')

    def action_notification(self):
        action = self.env.ref('om_hospital.action_hospital_patient')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Click to open the patient record'),
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient',
                }],
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'hospital.patient',
                    'res_id': self.patient_id.id,
                    'views': [(False, 'form')],
                }
            }
        }

    def action_test(self):
        # url action
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': 'https://www.odoo.com/'
        }

    def action_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_("There is no phone number for this patient in the record !"))
        message = 'Hi %s, your appointment number is: %s' % (self.patient_id.name, self.seq)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone, message)
        self.message_post(body=message, subject='Whatsapp Message')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

    def action_mail(self):
        template = self.env.ref('om_hospital.appointment_mail_template')
        for rec in self:
            if rec.patient_id.email:
                template.send_mail(rec.id, force_send=True)

    def action_consult(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Done',
                'type': 'rainbow_man',
            }

        }

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('state')
    def compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = 25
            elif rec.state == 'in_consultation':
                progress = 50
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress


class AppointmentPharmacy(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    sl_no = fields.Integer(string="SL No.")
    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')
    price_subtotal = fields.Monetary(string='Subtotal', compute='compute_price_subtotal')

    @api.depends('price_unit', 'qty')
    def compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty
