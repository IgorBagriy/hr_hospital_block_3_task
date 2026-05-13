from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DoctorCategory(models.Model):
    """Model representing doctor qualification categories."""

    _name = "hr.hospital.category"
    _description = "Doctor Qualification"
    _order = "sequence"

    name = fields.Char(string="Name", required=True, translate=True)
    sequence = fields.Integer(string="Sequence", default=10)
    doctor_ids = fields.One2many(
        comodel_name="hr.hospital.doctor",
        inverse_name="category_id",
        string="Doctors",
    )

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Category name must be unique!'),
    ]

    @api.constrains('name')
    def _check_name_unique(self):
        """Ensure that the category name is unique via Python logic."""
        for rec in self:
            domain = [('name', '=', rec.name), ('id', '!=', rec.id)]
            if self.search_count(domain) > 0:
                raise ValidationError("This category name already exists!")
