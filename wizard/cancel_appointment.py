from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment',
                                     domain=[('priority', 'in', ('0', '1', False))])
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = date.today()
        return res

    def action_cancel_appointment(self):
        if self.appointment_id.booking_date == fields.Date.today():
            raise ValidationError(_("Sorry! Cancellation is not allowed on the same day of booking!"))
        cancel_day = self.env['ir.config_parameter'].get_param('bm_hospital.cancel_day')
        allowed_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        if allowed_date < date.today():
            # print(allowed_date, date.today())
            raise ValidationError(_("Sorry! Cancellation is not allowed for this booking!"))
        self.appointment_id.state = 'cancel'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
