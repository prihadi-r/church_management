# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchSundaySchoolSessionStatus(models.Model):
    _name = 'church.sunday.school.session.status'
    _description = 'Master: Sunday School Session Status'
    _order = 'sequence, id'

    # Status sesi pertemuan: Planned, In Progress, Done, Cancelled.
    name = fields.Char(string='Status', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The session status code must be unique.'),
    ]
