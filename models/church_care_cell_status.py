# -*- coding: utf-8 -*-
from odoo import models, fields


class ChurchCareCellStatus(models.Model):
    _name = 'church.care.cell.status'
    _description = 'Master: Care Cell Status'
    _order = 'sequence, id'

    # Status alur care cell: Proposal, Review, Approved, Running,
    # Pending, Cancel, Stop (di-manage sebagai master, bukan selection)
    name = fields.Char(string='Status', required=True, translate=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(string='Active', default=True)
