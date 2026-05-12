from odoo import fields, models, api

class DoctorHistory(models.Model):

    _name = "hr.hospital.doctor.history"
    _description = "Doctor Personal History"

    patient_id = fields.Many2one("hr.hospital.patient", string="Patient", required=True)
    doctor_id = fields.Many2one("hr.hospital.doctor", string="Doctor", required=True)
    appointment_date = fields.Date(string="Appointment Date", required=True, default=fields.Date.today)
    change_date = fields.Date(string="Change Date")
    active = fields.Boolean(default=True)

    @api.onchange('appointment_date', 'change_date')
    def _onchange_dates(self):
        if self.appointment_date and self.change_date:
            if self.change_date < self.appointment_date:
                return {
                    'warning': {
                        'title': "Невідповідність дат",
                        'message': "Дата зміни лікаря не може бути раніше ніж дата призначення"
                    }
                }
        return {}

    @api.depends('patient_id', 'doctor_id', 'appointment_date')
    def _compute_display_name(self):
        for rec in self:
            p_name = rec.patient_id.name or "Unknown Patient"
            d_name = rec.doctor_id.name or "Unknown Doctor"
            category = rec.doctor_id.category_id.name or "Без категорії"
            rec.display_name = f"{p_name} - {d_name} ({category}) {rec.appointment_date}"
