from odoo import fields, models


class MassReassignDoctorWizard(models.TransientModel):
    """Wizard for mass reassigning personal doctors to selected patients."""

    _name = 'mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Personal Doctor'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Doctor',
        required=True,
    )
    reassign_date = fields.Date(
        string='Reassign Date',
        default=fields.Date.today,
        required=True,
    )

    def action_reassign(self):
        self.ensure_one()

        active_patient_ids = self.env.context.get('active_ids') or []
        patients = self.env['hr.hospital.patient'].browse(active_patient_ids)

        history_vals_list = []

        for patient in patients:
            old_history = self.env['hospital.doctor.history'].search(
                [('patient_id', '=', patient.id), ('active', '=', True)], limit=1
            )

            if old_history:
                old_history.write({'change_date': self.reassign_date, 'active': False})

            patient.personal_doctor_id = self.doctor_id

            history_vals_list.append(
                {
                    'patient_id': patient.id,
                    'doctor_id': self.doctor_id.id,
                    'appointment_date': self.reassign_date,
                    'active': True,
                }
            )

        if history_vals_list:
            self.env['hospital.doctor.history'].create(history_vals_list)

        return {'type': 'ir.actions.act_window_close'}
