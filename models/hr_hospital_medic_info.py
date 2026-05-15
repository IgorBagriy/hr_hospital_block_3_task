from datetime import date

from odoo import api, fields, models


class HospitalMedicInfo(models.AbstractModel):
    """Abstract model providing shared medical fields for doctors and patients."""

    _name = 'hospital.medic.info'
    _description = 'Abstract Medical Info'

    blood_group = fields.Selection(
        selection=[
            ('0_pos', 'O(I) Rh+'),
            ('0_neg', 'O(I) Rh-'),
            ('a_pos', 'A(II) Rh+'),
            ('a_neg', 'A(II) Rh-'),
            ('b_pos', 'B(III) Rh+'),
            ('b_neg', 'B(III) Rh-'),
            ('ab_pos', 'AB(IV) Rh+'),
            ('ab_neg', 'AB(IV) Rh-'),
        ],
        string='Blood Group',
    )
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        string='Gender',
    )
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=False,
    )

    @api.depends('birth_date')
    def _compute_age(self):
        """Calculate the current age dynamically based on the birth date."""
        today = date.today()
        for rec in self:
            if rec.birth_date:
                is_before_birthday = (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                rec.age = today.year - rec.birth_date.year - is_before_birthday
            else:
                rec.age = 0
