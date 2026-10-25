# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchMissionRole(models.Model):
    _name = 'church.mission.role'
    _description = 'Master: Mission Participant Role'
    _order = 'sequence, id'

    # Peran peserta dalam tim misi: ketua tim, anggota, tenaga medis, dll.
    name = fields.Char(string='Role', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The mission role code must be unique.'),
    ]
