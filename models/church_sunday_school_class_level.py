# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchSundaySchoolClassLevel(models.Model):
    _name = 'church.sunday.school.class.level'
    _description = 'Master: Sunday School Class Level'
    _order = 'sequence, name'

    # Tingkat kelas sekolah minggu (Batita, TK, SD, Remaja, dst).
    # Dikelola sebagai master agar tidak memakai selection field.
    name = fields.Char(string='Level Name', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The class level code must be unique.'),
    ]
