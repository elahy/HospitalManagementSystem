from odoo import api, fields, models


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    reason = fields.Text(string="Reason")
    # active = fields.Boolean(string='Active', default=True)
    # color = fields.Integer(string='Color')
    # other_color = fields.Char(string='Other Color')

    def action_cancel_appointment(self):

        pass