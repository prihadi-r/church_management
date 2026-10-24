# -*- coding: utf-8 -*-
from datetime import date

from odoo import api, fields, models


class ChurchSundaySchoolStudent(models.Model):
    _name = 'church.sunday.school.student'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Sunday School Student'
    _order = 'name'

    # Delegasi ke res.partner: nama, telepon, email, dan alamat otomatis
    # tersedia di model ini (tanpa duplikasi field).
    partner_id = fields.Many2one(
        'res.partner', string='Contact',
        required=True, ondelete='cascade', auto_join=True, index=True)

    code = fields.Char(string='Student Code', readonly=True, copy=False)
    birth_date = fields.Date(string='Date of Birth')
    age = fields.Integer(
        string='Age', compute='_compute_age', store=True)

    # Referensi master (bukan selection field)
    class_id = fields.Many2one(
        'church.sunday.school.class', string='Class', index=True)
    status_id = fields.Many2one(
        'church.sunday.school.student.status', string='Status',
        ondelete='restrict')

    enrollment_date = fields.Date(
        string='Enrollment Date', default=fields.Date.context_today)
    guardian_id = fields.Many2one(
        'res.partner', string='Parent / Guardian', ondelete='restrict')

    attendance_ids = fields.One2many(
        'church.sunday.school.attendance', 'student_id', string='Attendance')

    session_count = fields.Integer(
        string='Sessions', compute='_compute_attendance_stats', store=True)
    present_count = fields.Integer(
        string='Present', compute='_compute_attendance_stats', store=True)
    absent_count = fields.Integer(
        string='Absent', compute='_compute_attendance_stats', store=True)
    attendance_rate = fields.Float(
        string='Attendance Rate (%)', compute='_compute_attendance_stats',
        store=True, digits=(5, 2))

    color = fields.Integer(
        string='Color Index', compute='_compute_color', store=True)

    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('partner_uniq', 'unique(partner_id)',
         'This contact is already registered as a Sunday school student.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('status_id'):
                vals['status_id'] = self._default_status_id()
        records = super().create(vals_list)
        for record in records:
            if not record.code:
                record.code = self.env['ir.sequence'].next_by_code(
                    'church.sunday.school.student') or '/'
        return records

    @api.model
    def _default_status_id(self):
        status = self.env['church.sunday.school.student.status'].search(
            [('code', '=', 'active')], limit=1)
        if not status:
            status = self.env['church.sunday.school.student.status'].search([], limit=1)
        return status.id

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birth_date:
                born = record.birth_date
                record.age = today.year - born.year - (
                    (today.month, today.day) < (born.month, born.day))
            else:
                record.age = 0

    @api.depends('attendance_ids.present')
    def _compute_attendance_stats(self):
        for record in self:
            total = len(record.attendance_ids)
            present = len(record.attendance_ids.filtered('present'))
            record.session_count = total
            record.present_count = present
            record.absent_count = total - present
            record.attendance_rate = (present * 100.0 / total) if total else 0.0

    @api.depends('status_id.color')
    def _compute_color(self):
        for record in self:
            record.color = record.status_id.color or 0
