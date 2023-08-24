# -*- coding: utf-8 -*-
from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = "mail.thread", "mail.activity.mixin"
    _description = "Hospital Patient"

    name = fields.Char(string='Patient Name', tracking=True)
    dob = fields.Date(string="Date of Birth")
    ref = fields.Char(string='Reference', tracking=True)
    age = fields.Integer(string='Age', compute='compute_age', inverse='inverse_compute_age', search='search_age', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    active = fields.Boolean(string='Active', default=True)
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    doctor_ids = fields.Many2many('res.users', compute='_compute_doctors', string="Appointments")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')],
                                      string="Marital Status", tracking=True)
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string="Birthday ?", compute='compute_is_birthday')
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.depends('doctor_ids')
    def _compute_doctors(self):
        for rec in self:
            rec.doctor_ids = self.env['hospital.appointment'].search([('patient_id', '=', rec.id)]).doctor_id

    @api.constrains('dob')
    def _check_dob(self):
        for rec in self:
            if rec.dob and rec.dob > fields.Date.today():
                raise ValidationError(_("Invalid date of birth !"))

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("Cannot delete patient with appointment(s) !"))

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    @api.depends('dob')
    def compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    @api.depends('age')
    def inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.dob = today - relativedelta.relativedelta(years=rec.age)
        return

    def search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('dob', '>=', start_of_year), ('dob', '<=', end_of_year)]

    def name_get(self):
        patient_list = []
        for record in self:
            name = '[' + record.ref + ']' + ' ' + record.name
            patient_list.append((record.id, name))

        return patient_list
        # return [(record.id,"[%s] %s" % (record.ref, record.name)) for record in self]

    def action_test(self):
        print("Clicked...!")
        return

    @api.depends('dob')
    def compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.dob:
                today = date.today()
                if today.day == rec.dob.day and today.month == rec.dob.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    def action_view_appointments(self):
        return{
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form,calendar,activity',
            'context':{'default_patient_id': self.id},
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }
