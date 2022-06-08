from odoo import api, fields, models


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one(string='Name')
    active = fields.Boolean(string='Active', default=True)
    color = fields.Integer(string='Color')
    other_color = fields.Char(string='Other Color')