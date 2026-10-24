# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchSundaySchoolClassTeacher(models.Model):
    _name = 'church.sunday.school.class.teacher'
    _description = 'Sunday School Class Teacher'
    _order = 'class_id, teacher_id'

    # Pivot guru per kelas: satu guru bisa mengajar beberapa kelas
    # dengan peran yang berbeda (Kepala Sekolah, Guru Kelas, Asisten, dst).
    class_id = fields.Many2one(
        'church.sunday.school.class', string='Class',
        required=True, ondelete='cascade', index=True)
    teacher_id = fields.Many2one(
        'church.sunday.school.teacher', string='Teacher',
        required=True, ondelete='cascade', index=True)
    role_id = fields.Many2one(
        'church.sunday.school.teacher.role', string='Role', ondelete='restrict')
    since_date = fields.Date(string='Assigned Since')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('class_teacher_uniq', 'unique(class_id, teacher_id)',
         'This teacher is already assigned to this class.'),
    ]
