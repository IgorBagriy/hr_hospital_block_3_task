from odoo.exceptions import ValidationError
from odoo import fields, models, api

class DoctorCategory(models.Model):

    _name = "hr.hospital.category"
    _description = "Doctor Qualification"
    _order = "sequence"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    doctor_ids = fields.One2many(
        comodel_name="hr.hospital.doctor",
        inverse_name="category_id",
        string="Doctors"
    )

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Назва категорії має бути унікальною!'),
    ]

    @api.constrains('name')
    def _check_name_unique(self):
        for rec in self:
            domain = [('name', '=', rec.name), ('id', '!=', rec.id)]
            if self.search_count(domain) > 0:
                raise ValidationError("Така назва категорії вже існує!")
