# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchMissionaryStatus(models.Model):
    _name = 'church.missionary.status'
    _description = 'Master: Missionary Status'
    _order = 'sequence, id'

    # Tahapan pelayanan misionaris: Candidate, Preparing, On the Field,
    # Furlough, Completed.
    name = fields.Char(string='Status', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')
    is_closed = fields.Boolean(
        string='Closed Status',
        help='Missionaries in this status are no longer active on the field.')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The missionary status code must be unique.'),
    ]
