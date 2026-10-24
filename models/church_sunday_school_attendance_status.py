# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchSundaySchoolAttendanceStatus(models.Model):
    _name = 'church.sunday.school.attendance.status'
    _description = 'Master: Sunday School Attendance Status'
    _order = 'sequence, id'

    # Status kehadiran: Present, Late, Permission, Sick, Absent.
    # is_present dipakai untuk menghitung rekap & persentase kehadiran.
    name = fields.Char(string='Status', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')
    is_present = fields.Boolean(string='Counts as Present', default=False)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The attendance status code must be unique.'),
    ]
