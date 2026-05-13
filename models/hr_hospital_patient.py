from odoo import fields, models


class HospitalPatient(models.Model):
    """Model representing patients receiving treatment and their doctor history."""

    _name = "hr.hospital.patient"
    _description = "Hospital Patient"
    _inherit = ["hr.hospital.medic.info"]

    name = fields.Char(string="Full Name", required=True)
    personal_doctor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        string="Personal Doctor",
    )
    doctor_history_ids = fields.One2many(
        comodel_name="hr.hospital.doctor.history",
        inverse_name="patient_id",
        string="Doctor History",
        readonly=True,
    )
    insurance_number = fields.Char(
        string="Insurance Number",
        size=20,
    )

