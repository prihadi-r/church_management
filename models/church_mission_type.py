# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchMissionType(models.Model):
    _name = 'church.mission.type'
    _description = 'Master: Mission Type'
    _order = 'sequence, name'

    # Jenis misi: penginjilan, penanaman gereja, medis, pendidikan, dll.
    name = fields.Char(string='Mission Type', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'The mission type code must be unique.'),
    ]
