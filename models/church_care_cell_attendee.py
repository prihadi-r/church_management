# -*- coding: utf-8 -*-
from odoo import models, fields


class ChurchCareCellAttendee(models.Model):
    _name = 'church.care.cell.attendee'
    _description = 'Pivot: Care Cell Attendee'

    # Sub-class dari care cell: mencatat peserta/anggota (link ke kontak)
    care_cell_id = fields.Many2one(
        'church.care.cell', string='Care Cell', required=True, ondelete='cascade')
    partner_id = fields.Many2one(
        'res.partner', string='Attendee', required=True)
    role = fields.Selection([
        ('leader', 'Leader'),
        ('member', 'Member'),
        ('guest', 'Guest'),
    ], string='Role', default='member')
    joined_date = fields.Date(string='Joined Date')
    notes = fields.Text(string='Notes')
