from odoo import fields, models, api
from odoo.exceptions import ValidationError

class HospitalDoctor(models.Model):

    _name = "hr.hospital.doctor"
    _description = "Hospital Doctor"
    _inherit = ["hr.hospital.medic.info"]

    name = fields.Char(string="Full Name", required=True)

    specialization = fields.Char(string="Specialization")
    category_id = fields.Many2one("hr.hospital.category", string="Категорія")
    user_id = fields.Many2one("res.users", string="Користувач системи")
    is_intern = fields.Boolean(string="Лікар є інтерном", compute="_compute_is_intern", store=True)
    mentor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        string="Ментор",
    )

    @api.depends('name')
    def _compute_display_name(self):
        for rec in self:
            if rec.name:
                rec.display_name = f"Dr. {rec.name}"
            else:
                rec.display_name = "New Doctor"

    @api.depends('category_id')
    def _compute_is_intern(self):
        for rec in self:
            # Назва категорії з вашого data-файлу
            rec.is_intern = rec.category_id.name == "Лікар-інтерн"

    @api.constrains('mentor_id')
    def _check_mentor(self):
        for rec in self:
            if rec.mentor_id and rec.mentor_id.is_intern:
                raise ValidationError("Ментор не може бути інтерном!")

    @api.constrains('mentor_id')
    def _check_mentor_not_self(self):
        for rec in self:
            # rec.id — це ID поточного запису
            # rec.mentor_id.id — це ID вибраного ментора
            if rec.mentor_id and rec.mentor_id.id == rec.id:
                raise ValidationError("Помилка! Лікар не може бути ментором самому собі.")
