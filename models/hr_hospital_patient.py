from odoo import fields, models

class HospitalPatient(models.Model):

    _name = "hr.hospital.patient"
    _description = "Hospital Patient"
    _inherit = ["hr.hospital.medic.info"]

    name = fields.Char(string="Full Name", required=True)

    personal_doctor_id = fields.Many2one("hr.hospital.doctor", string="Персональний лікар")
    doctor_history_ids = fields.One2many(
        "hr.hospital.doctor.history", "patient_id", string="Історія персональних лікарів", readonly=True
    )
    insurance_number = fields.Char(string="Номер страхового поліса", size=20)
