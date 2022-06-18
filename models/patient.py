from datetime import date
from odoo.exceptions import ValidationError
from odoo import api, fields, models, _
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', tracking=True, required=True)
    date_of_birth = fields.Date(string='Date Of Birth', tracking=True, required=True)
    ref = fields.Char(string='Reference')
    age = fields.Integer(string='Age', compute='_compute_age', inverse='_inverse_compute_age',
                         search='_search_age', tracking=True, required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], required=True, tracking=True, string='Gender')
    active = fields.Boolean(string="Active", default=True)
    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string="Appointments")
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string='Tags')
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    parent = fields.Char(string='Parent Name')
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string="Marital Status",
                                      tracking=True)
    partner_name = fields.Char(string='Partner Name')
    is_birthday = fields.Boolean(string="Birthday ?", compute='_compute_is_birthday')
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("Please Enter the Correct Date of Birth! "))

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("You cannot delete a patient with appointments !"))

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            if rec.age:
                rec.date_of_birth = today - relativedelta.relativedelta(year=rec.age)
            # else:
            #     rec.age = 0

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    def name_get(self):
        # patient_list = []
        # for record in self:
        #     name = record.ref + record.name
        #     patient_list.append((record.id, name))
        # return patient_list
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]

    def action_test(self):
        print("Clicked")
        return
    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

