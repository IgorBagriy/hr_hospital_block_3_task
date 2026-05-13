from odoo import fields, models
from odoo.exceptions import ValidationError


class HospitalVisit(models.Model):
    """Model representing patient visits to doctors and their statuses."""

    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'

    visit_date = fields.Datetime(
        string='Visit Date',
        default=fields.Datetime.now,
        required=True,
    )
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
        """Prevent modification of critical fields for completed visits."""
        for rec in self:
            if rec.state == 'completed':
                forbidden_fields = ['planned_date', 'actual_date', 'doctor_id', 'patient_id']
                if any(f in vals for f in forbidden_fields):
                    raise ValidationError('It is forbidden to change data of a completed visit!')
        return super().write(vals)

    def unlink(self):
        """Prevent deletion of completed visits."""
        for rec in self:
            if rec.state == 'completed':
                raise ValidationError('Completed visits cannot be deleted!')
        return super().unlink()
