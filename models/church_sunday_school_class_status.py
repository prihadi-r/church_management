# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchSundaySchoolClassStatus(models.Model):
    _name = 'church.sunday.school.class.status'
    _description = 'Master: Sunday School Class Status'
    _order = 'sequence, id'

    # Status kelas: Planned, Running, Completed, Cancelled.
    name = fields.Char(string='Status', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The class status code must be unique.'),
    ]
