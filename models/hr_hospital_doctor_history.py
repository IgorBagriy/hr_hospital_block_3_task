from odoo import api, fields, models


class DoctorHistory(models.Model):
    """Model representing historical tracking of patient's personal doctors."""

    _name = "hr.hospital.doctor.history"
    _description = "Doctor Personal History"

    patient_id = fields.Many2one(
        "hr.hospital.patient",
        string="Patient",
        required=True,
    )
    doctor_id = fields.Many2one(
        "hr.hospital.doctor",
        string="Doctor",
        required=True,
    )
    appointment_date = fields.Date(
        string="Appointment Date",
        required=True,
        default=fields.Date.today,
    )
    change_date = fields.Date(string="Change Date")
    active = fields.Boolean(string="Active", default=True)

    @api.onchange('appointment_date', 'change_date')
    def _onchange_dates(self):
        """Warn user if change date occurs before appointment date."""
        if self.appointment_date and self.change_date:
            if self.change_date < self.appointment_date:
                return {
                    'warning': {
                        'title': "Date Mismatch",
                        'message': (
                            "The doctor change date cannot be earlier "
                            "than the appointment date."
                        )
                    }
                }
        return {}

    @api.depends(
        'patient_id.name',
        'doctor_id.name',
        'doctor_id.category_id.name',
        'appointment_date'
    )
    def _compute_display_name(self):
        """Generate a structured display name for the history log."""
        for rec in self:
            p_name = rec.patient_id.name or "Unknown Patient"
            d_name = rec.doctor_id.name or "Unknown Doctor"
            category = rec.doctor_id.category_id.name or "No Category"
            date_str = rec.appointment_date or ""
            rec.display_name = f"{p_name} - {d_name} ({category}) {date_str}"
