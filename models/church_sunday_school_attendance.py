# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ChurchSundaySchoolAttendance(models.Model):
    _name = 'church.sunday.school.attendance'
    _description = 'Sunday School Attendance'
    _order = 'session_id, student_id'

    session_id = fields.Many2one(
        'church.sunday.school.session', string='Session',
        required=True, ondelete='cascade', index=True)
    class_id = fields.Many2one(
        'church.sunday.school.class', string='Class',
        related='session_id.class_id', store=True, index=True)
    student_id = fields.Many2one(
        'church.sunday.school.student', string='Student',
        required=True, ondelete='cascade', index=True)
    status_id = fields.Many2one(
        'church.sunday.school.attendance.status', string='Attendance Status',
        ondelete='restrict')
    # Nilai tersimpan dari status master, dipakai untuk rekap kehadiran.
    present = fields.Boolean(
        string='Present', related='status_id.is_present', store=True)
    note = fields.Text(string='Note')

    _sql_constraints = [
        ('session_student_uniq', 'unique(session_id, student_id)',
         'This student already has an attendance line for this session.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('status_id'):
                vals['status_id'] = self._default_status_id()
        return super().create(vals_list)

    @api.model
    def _default_status_id(self):
        status = self.env['church.sunday.school.attendance.status'].search(
            [('is_present', '=', True)], limit=1)
        if not status:
            status = self.env['church.sunday.school.attendance.status'].search([], limit=1)
        return status.id
