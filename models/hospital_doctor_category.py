from odoo import fields, models


class DoctorCategory(models.Model):
    """Model representing doctor qualification categories."""

    _name = 'hospital.doctor.category'
    _description = 'Doctor Qualification'
    _order = 'sequence'

    name = fields.Char(string='Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence', default=10)
    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='category_id',
        string='Doctors',
    )

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Category name must be unique!'),
    ]
