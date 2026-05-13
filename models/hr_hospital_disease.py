from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDisease(models.Model):
    """Model representing hospital disease hierarchy."""

    _name = "hr.hospital.disease"
    _description = "Disease Type"
    _parent_store = True
    _parent_name = "parent_id"

    name = fields.Char(string="Disease Name", required=True, translate=True)
    description = fields.Text(string="Description")
    parent_id = fields.Many2one(
        comodel_name="hr.hospital.disease",
        string="Parent Category",
        ondelete="cascade",
        index=True,
    )
    parent_path = fields.Char(index=True, unaccent=False)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        """Ensure that the disease hierarchy contains no recursion loops."""
        if not self._check_recursion():
            raise ValidationError(
                "Error! You cannot assign a disease as a parent to itself "
                "or its descendants."
            )

    def _compute_display_name(self):
        """Generate the full hierarchical string path for display name."""
        for rec in self:
            res = rec.name or ""
            current = rec.parent_id
            while current:
                res = f"{current.name} / {res}"
                current = current.parent_id
            rec.display_name = res
