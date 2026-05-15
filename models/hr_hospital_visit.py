from odoo import fields, models
from odoo.exceptions import ValidationError


class HospitalVisit(models.Model):
    """Model representing patient visits to doctors and their statuses."""

    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'

    active = fields.Boolean(string='Active', default=True)
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Final Diagnosis',
    )
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='planned',
        required=True,
    )
    planned_date = fields.Datetime(string='Planned Date')
    actual_date = fields.Datetime(string='Actual Date')
    summary = fields.Html(string='Epicrisis')

    def write(self, vals):
        for rec in self:
            if rec.state == 'completed':
                forbidden_fields = ['planned_date', 'actual_date', 'doctor_id', 'patient_id']
                if any(f in vals for f in forbidden_fields):
                    raise ValidationError('It is forbidden to change data of a completed visit!')
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state == 'completed':
                raise ValidationError('Completed visits cannot be deleted!')
        return super().unlink()

    def toggle_active(self):
        """Prevent archiving of completed visits."""
        for rec in self:
            if rec.state == 'completed':
                raise ValidationError('Completed visits cannot be archived or de-archived!')
        return super().toggle_active()
