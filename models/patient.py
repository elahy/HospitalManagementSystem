from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', tracking=True, required=True)
    ref = fields.Char(string='Reference', required=True, default="Self")
    age = fields.Integer(string='Age', tracking=True, required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], required=True, tracking=True, string='Gender')
    active = fields.Boolean(string="Active", default=True)

