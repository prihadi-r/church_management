# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EventEvent(models.Model):
    _inherit = 'event.event'

    # Mapping petugas ke event yang dijadwalkan
    roster_ids = fields.One2many('church.event.roster', 'event_id', string='Service Roster')
    
    # Field state untuk Kanban view
    event_status = fields.Selection([
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('finished', 'Finished')
    ], string='Event Status', default='upcoming')

    # ===========================================
    # Auto-sync ke kalender kegiatan gereja
    # ===========================================
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            self.env['church.activity']._sync_from_event(record)
        return records

    def write(self, vals):
        res = super().write(vals)
        if any(field in vals for field in ('name', 'date_begin', 'date_end', 'active')):
            for record in self:
                self.env['church.activity']._sync_from_event(record)
        return res

    def unlink(self):
        self.env['church.activity'].search([('event_id', 'in', self.ids)]).unlink()
        return super().unlink()