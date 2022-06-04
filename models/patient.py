from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"

    name = fields.Char(string='Name', required=True)
    ref = fields.Char(string='Reference', required=True)
    age = fields.Integer(string='Age', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], required=True, string='Gender')
    active = fields.Boolean(string="Active", default=True)

