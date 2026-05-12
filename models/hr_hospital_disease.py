from odoo import fields, models, api
from odoo.exceptions import ValidationError

class HospitalDisease(models.Model):

    _name = "hr.hospital.disease"
    _description = "Disease Type"
    _parent_store = True
    _parent_name = "parent_id"

    name = fields.Char(string="Disease Name", required=True)
    description = fields.Text(string="Description")
    parent_id = fields.Many2one(
        comodel_name="hr.hospital.disease",
        string="Батьківська категорія",
        ondelete="cascade",
        index=True
    )
    parent_path = fields.Char(index=True, unaccent=False)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise ValidationError(
                "Помилка! Ви не можете призначити хворобу батьківською для самої себе або її нащадків.")

    def _compute_display_name(self):
        for rec in self:
            res = rec.name
            current = rec.parent_id
            while current:
                res = f"{current.name} / {res}"
                current = current.parent_id
            rec.display_name = res

