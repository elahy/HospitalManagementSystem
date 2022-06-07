from datetime import date
from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', tracking=True, required=True)
    date_of_birth = fields.Date(string='Date Of Birth', tracking=True, required=True)
    ref = fields.Char(string='Reference', required=True, default="Self")
    age = fields.Integer(string='Age', compute='_compute_age', tracking=True, required=True)
    gender = fields.Selection([('male', 'Male'),('female', 'Female')], required=True, tracking=True, string='Gender')
    active = fields.Boolean(string="Active", default=True)
    appointment_id = fields.Many2one(comodel_name='hospital.appointment', string="Appointments")
    image = fields.Image(string="Image")

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0