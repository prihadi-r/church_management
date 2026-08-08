# -*- coding: utf-8 -*-
from odoo import models, fields

class ChurchEventRoster(models.Model):
    _name = 'church.event.roster'
    _description = 'Pivot: Event Roster Assignment'

    # Relasi untuk mengikat Event, Person (Partner), dan Role
    event_id = fields.Many2one('event.event', string='Event', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Person', required=True)
    role_id = fields.Many2one('church.event.role', string='Role', required=True)