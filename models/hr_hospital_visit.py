from odoo import fields, models
from odoo.exceptions import ValidationError

class HospitalVisit(models.Model):

    _name = "hr.hospital.visit"
    _description = "Patient Visit"

    visit_date = fields.Datetime(
        string="Visit Date",
        default=fields.Datetime.now,
        required=True
    )

    doctor_id = fields.Many2one(
        "hr.hospital.doctor",
        string="Doctor",
        required=True)

    patient_id = fields.Many2one(
        "hr.hospital.patient",
        string="Patient",
        required=True)

    disease_id = fields.Many2one(
        "hr.hospital.disease",
        string="Final Diagnosis")

    state = fields.Selection([
        ('planned', 'Заплановано'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано')
    ], string="Статус", default='planned', required=True)

    planned_date = fields.Datetime(string="Запланована дата")
    actual_date = fields.Datetime(string="Дата та час візиту")
    summary = fields.Html(string="Epicrisis")

    def write(self, vals):
        for rec in self:
            if rec.state == 'completed' and any(f in vals for f in ['planned_date', 'actual_date', 'doctor_id', 'patient_id']):
                raise ValidationError("Неможливо змінити дані завершеного візиту!")
        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state == 'completed':
                raise ValidationError("Неможливо видалити завершений візит!")
        return super().unlink()