# -*- coding: utf-8 -*-
from odoo import models, fields


class ChurchCareCellSession(models.Model):
    _name = 'church.care.cell.session'
    _description = 'Care Cell Session'
    _order = 'date desc, id desc'

    # Sub-class dari care cell: rencana & catatan untuk tiap sesi pertemuan.
    # Wajib memiliki tanggal sesi (date).
    care_cell_id = fields.Many2one(
        'church.care.cell', string='Care Cell', required=True, ondelete='cascade')
    name = fields.Char(string='Session Title')
    date = fields.Date(string='Session Date', required=True)
    plan = fields.Text(string='Plan')
    note = fields.Text(string='Note')
