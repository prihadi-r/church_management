# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ChurchSundaySchoolClass(models.Model):
    _name = 'church.sunday.school.class'
    _description = 'Sunday School Class'
    _order = 'sequence, name'

    name = fields.Char(string='Class Name', required=True)
    code = fields.Char(string='Class Code', copy=False)
    sequence = fields.Integer(string='Sequence', default=10)

    # Referensi master (bukan selection field)
    level_id = fields.Many2one(
        'church.sunday.school.class.level', string='Class Level',
        required=True, ondelete='restrict')
    status_id = fields.Many2one(
        'church.sunday.school.class.status', string='Status', ondelete='restrict')

    teacher_id = fields.Many2one(
        'church.sunday.school.teacher', string='Head Teacher',
        ondelete='restrict')

    # Sub-class: guru pengajar kelas ini (bisa lebih dari satu)
    teacher_ids = fields.One2many(
        'church.sunday.school.class.teacher', 'class_id', string='Teachers')
    # Sub-class: murid yang terdaftar di kelas ini
    student_ids = fields.One2many(
        'church.sunday.school.student', 'class_id', string='Students')
    # Sub-class: sesi pertemuan & absensi kelas
    session_ids = fields.One2many(
        'church.sunday.school.session', 'class_id', string='Sessions')

    room = fields.Char(string='Room')
    meeting_time = fields.Float(
        string='Weekly Meeting Time',
        help='Jam pertemuan rutin (contoh: 08:00).')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    capacity = fields.Integer(string='Capacity')

    student_count = fields.Integer(
        string='Students Count', compute='_compute_counts', store=True)
    teacher_count = fields.Integer(
        string='Teachers Count', compute='_compute_counts', store=True)
    session_count = fields.Integer(
        string='Sessions Count', compute='_compute_counts', store=True)
    next_session_datetime = fields.Datetime(
        string='Next Session', compute='_compute_next_session_datetime', store=True)

    # Indeks warna kartu Kanban & Kalender (mengikuti warna status)
    color = fields.Integer(
        string='Color Index', compute='_compute_color', store=True)

    active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        # Default status dipasang di create (bukan default field) agar tidak
        # melakukan query DB saat schema update.
        for vals in vals_list:
            if not vals.get('status_id'):
                vals['status_id'] = self._default_status_id()
        return super().create(vals_list)

    def unlink(self):
        # Sesi dihapus via cascade di DB, jadi baris kalender harus
        # dibersihkan lebih dulu di level ORM.
        self.env['church.activity'].search(
            [('sunday_school_session_id', 'in', self.session_ids.ids)]).unlink()
        return super().unlink()

    @api.model
    def _default_status_id(self):
        status = self.env['church.sunday.school.class.status'].search(
            [('code', '=', 'planned')], limit=1)
        if not status:
            status = self.env['church.sunday.school.class.status'].search([], limit=1)
        return status.id

    @api.depends('student_ids', 'teacher_ids', 'session_ids')
    def _compute_counts(self):
        for record in self:
            record.student_count = len(record.student_ids)
            record.teacher_count = len(record.teacher_ids)
            record.session_count = len(record.session_ids)

    @api.depends('session_ids.start_datetime', 'session_ids.status_id.code')
    def _compute_next_session_datetime(self):
        now = fields.Datetime.now()
        for record in self:
            sessions = record.session_ids.filtered(
                lambda s: s.start_datetime and s.status_id.code != 'cancel')
            starts = sessions.mapped('start_datetime')
            if not starts:
                record.next_session_datetime = False
                continue
            upcoming = [start for start in starts if start >= now]
            record.next_session_datetime = (
                min(upcoming) if upcoming else max(starts))

    @api.depends('status_id.color')
    def _compute_color(self):
        for record in self:
            record.color = record.status_id.color or 0

    @api.constrains('capacity')
    def _check_capacity(self):
        for record in self:
            if record.capacity < 0:
                raise ValidationError(_('Capacity cannot be negative.'))
