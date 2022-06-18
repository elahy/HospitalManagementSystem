from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'name'
    _order = 'id desc'

    name = fields.Char(string='Sequence', default='New')
    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient", ondelete='restrict')
    gender = fields.Selection([('male', 'Male'),('female', 'Female')], string='Gender', related='patient_id.gender')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string='Reference')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], string="Status", default='draft', tracking=True, required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor')
    pharmacy_detail_ids = fields.One2many('appointment.pharmacy.details', 'appointment_id', string='Pharmacy Details')
    hide_sales_price = fields.Boolean(string="Hide Sales Price")
    operation_id = fields.Many2one(comodel_name='hospital.operation', string="Operation")
    progress = fields.Integer(string="Progress", compute='_compute_progress')
    duration = fields.Float(string="Duration")

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_("You can delete appointment only in 'draft' state ! "))
            return super(HospitalAppointment, self).unlink()

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).create(vals) v

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        print("Hello World, Button Clicked")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Object Button Working Perfectly!',
                'type': 'rainbow_man',
            }
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref('bm_hospital.action_cancel_appointment').read()[0]
        return action
        # for rec in self:
        #     rec.state = 'cancel'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('state')
    def _compute_progress(self):
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


class AppointmentPharmacyDetails(models.Model):
    _name = "appointment.pharmacy.details"
    _description = "Appointment Pharmacy Details"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string='Price', related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')