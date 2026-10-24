# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchSundaySchoolTeacherRole(models.Model):
    _name = 'church.sunday.school.teacher.role'
    _description = 'Master: Sunday School Teacher Role'
    _order = 'sequence, name'

    # Peran pengajar (Kepala Sekolah, Guru Kelas, Asisten, Pengganti, dst).
    name = fields.Char(string='Role Name', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The teacher role code must be unique.'),
    ]
