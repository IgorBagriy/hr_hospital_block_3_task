from odoo import fields, models, api
from odoo.exceptions import ValidationError

class HospitalDoctor(models.Model):
    """Hospital Doctor personnel records."""

    _name = "hr.hospital.doctor"
    _description = "Hospital Doctor"

    name = fields.Char(string="Full Name", required=True)

    specialization = fields.Char(string="Specialization")
    mentor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        string="Mentor Doctor",
    )

    @api.depends('name')
    def _compute_display_name(self):
        for rec in self:
            if rec.name:
                rec.display_name = f"Dr. {rec.name}"
            else:
                rec.display_name = "New Doctor"

    @api.constrains('mentor_id')
    def _check_mentor_not_self(self):
        for rec in self:
            # rec.id — це ID поточного запису
            # rec.mentor_id.id — це ID вибраного ментора
            if rec.mentor_id and rec.mentor_id.id == rec.id:
                raise ValidationError("Помилка! Лікар не може бути ментором самому собі.")
