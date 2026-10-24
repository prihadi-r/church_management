# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models


class ChurchSundaySchoolSession(models.Model):
    _name = 'church.sunday.school.session'
    _description = 'Sunday School Session'
    _order = 'start_datetime desc, id desc'

    name = fields.Char(string='Topic', required=True)
    class_id = fields.Many2one(
        'church.sunday.school.class', string='Class',
        required=True, ondelete='cascade', index=True)
    teacher_id = fields.Many2one(
        'church.sunday.school.teacher', string='Teacher', ondelete='restrict')
    start_datetime = fields.Datetime(string='Start', required=True)
    end_datetime = fields.Datetime(string='End')
    calendar_stop = fields.Datetime(
        string='Calendar End', compute='_compute_calendar_stop', store=True)

    status_id = fields.Many2one(
        'church.sunday.school.session.status', string='Status',
        ondelete='restrict')

    lesson_summary = fields.Text(string='Lesson Summary')
    notes = fields.Text(string='Notes')

    attendance_ids = fields.One2many(
        'church.sunday.school.attendance', 'session_id', string='Attendance')

    attendance_count = fields.Integer(
        string='Students', compute='_compute_attendance_counts', store=True)
    present_count = fields.Integer(
        string='Present', compute='_compute_attendance_counts', store=True)
    absent_count = fields.Integer(
        string='Absent', compute='_compute_attendance_counts', store=True)

    color = fields.Integer(
        string='Color Index', compute='_compute_color', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('status_id'):
                vals['status_id'] = self._default_status_id()
        records = super().create(vals_list)
        for record in records:
            self.env['church.activity']._sync_from_sunday_school_session(record)
        return records

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            self.env['church.activity']._sync_from_sunday_school_session(record)
        return res

    def unlink(self):
        self.env['church.activity'].search(
            [('sunday_school_session_id', 'in', self.ids)]).unlink()
        return super().unlink()

    @api.model
    def _default_status_id(self):
        status = self.env['church.sunday.school.session.status'].search(
            [('code', '=', 'planned')], limit=1)
        if not status:
            status = self.env['church.sunday.school.session.status'].search([], limit=1)
        return status.id

    @api.depends('start_datetime', 'end_datetime')
    def _compute_calendar_stop(self):
        for record in self:
            record.calendar_stop = record.end_datetime or (
                record.start_datetime + timedelta(hours=1)
                if record.start_datetime else False)

    @api.depends('attendance_ids.present')
    def _compute_attendance_counts(self):
        for record in self:
            total = len(record.attendance_ids)
            present = len(record.attendance_ids.filtered('present'))
            record.attendance_count = total
            record.present_count = present
            record.absent_count = total - present

    @api.depends('status_id.color')
    def _compute_color(self):
        for record in self:
            record.color = record.status_id.color or 0

    def _set_status_by_code(self, code):
        status = self.env['church.sunday.school.session.status'].search(
            [('code', '=', code)], limit=1)
        if status:
            self.write({'status_id': status.id})

    def action_mark_in_progress(self):
        self._set_status_by_code('in_progress')

    def action_mark_done(self):
        self._set_status_by_code('done')

    def action_reset_to_planned(self):
        self._set_status_by_code('planned')

    def action_cancel(self):
        self._set_status_by_code('cancel')

    def action_generate_attendance(self):
        """Buat baris absensi untuk semua murid aktif kelas ini."""
        Attendance = self.env['church.sunday.school.attendance']
        default_status = Attendance._default_status_id()
        for session in self:
            existing = session.attendance_ids.mapped('student_id')
            students = session.class_id.student_ids.filtered('active') - existing
            vals_list = [{
                'session_id': session.id,
                'student_id': student.id,
                'status_id': default_status,
            } for student in students]
            if vals_list:
                Attendance.create(vals_list)
        return True
