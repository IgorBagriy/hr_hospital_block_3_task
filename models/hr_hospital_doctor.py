from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    """Model representing hospital doctor personnel."""

    _name = "hr.hospital.doctor"
    _description = "Hospital Doctor"
    _inherit = ["hr.hospital.medic.info"]

    name = fields.Char(string="Full Name", required=True)
    specialization = fields.Char(string="Specialization")
    category_id = fields.Many2one(
        "hr.hospital.category",
        string="Category",
    )
    user_id = fields.Many2one(
        "res.users",
        string="System User",
    )
    is_intern = fields.Boolean(
        string="Is Intern",
        compute="_compute_is_intern",
        store=True,
    )
    mentor_id = fields.Many2one(
        comodel_name="hr.hospital.doctor",
        string="Mentor Doctor",
    )

    @api.depends('name')
    def _compute_display_name(self):
        """Generate doctor display name with title."""
        for rec in self:
            if rec.name:
                rec.display_name = f"Dr. {rec.name}"
            else:
                rec.display_name = "New Doctor"

    @api.depends('category_id')
    def _compute_is_intern(self):
        """Check if the doctor is an intern based on XML External ID."""
        try:
            intern_category = self.env.ref('hr_hospital.cat_intern')
        except ValueError:
            intern_category = False

        for rec in self:
            if intern_category and rec.category_id == intern_category:
                rec.is_intern = True
            else:
                rec.is_intern = False

    @api.constrains('mentor_id')
    def _check_mentor(self):
        """Ensure that the selected mentor is not an intern."""
        for rec in self:
            if rec.mentor_id and rec.mentor_id.is_intern:
                raise ValidationError("Mentor cannot be an intern!")

    @api.constrains('mentor_id')
    def _check_mentor_not_self(self):
        """Ensure that the doctor does not select themselves as a mentor."""
        for rec in self:
            # rec.id — це ID поточного запису
            # rec.mentor_id.id — це ID вибраного ментора
            if rec.mentor_id and rec.mentor_id.id == rec.id:
                raise ValidationError("A doctor cannot be their own mentor.")
