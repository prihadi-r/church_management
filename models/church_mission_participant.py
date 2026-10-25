# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ChurchMissionParticipant(models.Model):
    _name = 'church.mission.participant'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Mission Participant'
    _order = 'trip_id, name'

    # Delegasi ke res.partner: identitas peserta memakai kontak yang sudah
    # ada di Contacts (nama, telepon, email, alamat).
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True,
        ondelete='cascade', auto_join=True, index=True)

    trip_id = fields.Many2one(
        'church.mission.trip', string='Mission Trip', required=True,
        ondelete='cascade', index=True)

    role_id = fields.Many2one(
        'church.mission.role', string='Role', ondelete='restrict')
    registration_date = fields.Date(
        string='Registration Date', default=fields.Date.context_today)
    confirmed = fields.Boolean(string='Confirmed')

    color_index = fields.Integer(
        string='Color', compute='_compute_color_index', store=True)
    notes = fields.Text(string='Internal Notes')

    _sql_constraints = [
        ('trip_partner_uniq', 'unique(trip_id, partner_id)',
         'This contact is already registered on this mission trip.'),
    ]

    @api.depends('role_id.color')
    def _compute_color_index(self):
        for record in self:
            record.color_index = record.role_id.color or 0
