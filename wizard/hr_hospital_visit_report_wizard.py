from odoo import fields, models, api

class VisitReportWizard(models.TransientModel):
    _name = 'hr.hospital.visit.report.wizard'
    _description = 'Visit Report Wizard'

    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Лікарі')
    patient_ids = fields.Many2many('hr.hospital.patient', string='Пацієнти')
    date_start = fields.Date(string='Початок періоду')
    date_end = fields.Date(string='Кінець періоду')
    only_completed = fields.Boolean(string='Лише завершені візити', default=True)
    disease_id = fields.Many2one('hr.hospital.disease', string='Хвороба')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids')

        if active_model == 'hr.hospital.doctor':
            res.update({'doctor_ids': [(6, 0, active_ids)]})
        elif active_model == 'hr.hospital.patient':
            res.update({'patient_ids': [(6, 0, active_ids)]})
        return res

    def action_get_report(self):
        self.ensure_one()

        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))
        if self.date_start:
            domain.append(('planned_date', '>=', self.date_start))
        if self.date_end:
            domain.append(('planned_date', '<=', self.date_end))
        if self.only_completed:
            domain.append(('state', '=', 'completed'))
        if self.disease_id:
            domain.append(('disease_id', '=', self.disease_id.id))

        return {
            'name': 'Filtered Visits',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
            'target': 'current',
        }
