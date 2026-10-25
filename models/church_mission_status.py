# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchMissionStatus(models.Model):
    _name = 'church.mission.status'
    _description = 'Master: Mission Trip Status'
    _order = 'sequence, id'

    # Status perjalanan misi: Planned, Ongoing, Completed, Cancelled.
    name = fields.Char(string='Status', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')

    # Penanda status akhir (dipakai untuk hitungan "selesai" tanpa
    # mengandalkan kode status tertentu).
    is_closed = fields.Boolean(
        string='Closed Status',
        help='Trips in this status are considered finished.')

    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The mission status code must be unique.'),
    ]
