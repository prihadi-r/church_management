# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchMissionField(models.Model):
    _name = 'church.mission.field'
    _description = 'Master: Mission Field'
    _order = 'sequence, name'

    # Wilayah/medan misi (bisa bertingkat: benua -> negara -> suku).
    name = fields.Char(string='Mission Field', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)

    parent_id = fields.Many2one(
        'church.mission.field', string='Parent Field', ondelete='restrict')
    child_ids = fields.One2many(
        'church.mission.field', 'parent_id', string='Sub Fields')

    # Master bawaan Odoo (bukan text bebas)
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    color = fields.Integer(string='Color Index')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'The mission field code must be unique.'),
    ]
