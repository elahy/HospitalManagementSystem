from odoo import api, fields, models, _


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True, copy=False)
    color = fields.Integer(string='Color')
    other_color = fields.Char(string='Other Color')
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
        default['sequence'] = 10
        return super(PatientTag, self).copy(default)

    _sql_constraints = [
        ('unique_tag_name', 'unique (name, active)', 'Name must be unique.'),
        ('check_sequence', 'check (sequence > 0)', 'Sequence must be non zero positive number.')
    ]
