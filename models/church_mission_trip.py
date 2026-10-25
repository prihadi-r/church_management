# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ChurchMissionTrip(models.Model):
    _name = 'church.mission.trip'
    _inherits = {'event.event': 'event_id'}
    _description = 'Mission Trip'
    _order = 'date_begin desc, id desc'

    # Delegasi ke event.event: nama, tanggal mulai/selesai, venue, deskripsi,
    # peserta terdaftar (event.registration), dan pengaturan tiket memakai
    # model Event. Dengan begitu perjalanan misi otomatis muncul di aplikasi
    # Events dan di Church Calendar (church.activity).
    event_id = fields.Many2one(
        'event.event', string='Event Record', required=True,
        ondelete='cascade', auto_join=True, index=True)

    code = fields.Char(string='Trip Code', readonly=True, copy=False)

    # Referensi master (bukan selection field)
    type_id = fields.Many2one(
        'church.mission.type', string='Mission Type', ondelete='restrict')
    field_id = fields.Many2one(
        'church.mission.field', string='Mission Field', ondelete='restrict')
    agency_id = fields.Many2one(
        'church.mission.agency', string='Sending Agency', ondelete='restrict')
    status_id = fields.Many2one(
        'church.mission.status', string='Status', ondelete='restrict')
    leader_id = fields.Many2one(
        'church.mission.missionary', string='Trip Leader', ondelete='set null')

    currency_id = fields.Many2one('res.currency', string='Currency')
    budget = fields.Monetary(string='Budget', currency_field='currency_id')
    support_total = fields.Monetary(
        string='Support Received', currency_field='currency_id',
        compute='_compute_support', store=True)
    funding_progress = fields.Float(
        string='Funding Progress (%)', compute='_compute_support',
        store=True, digits=(5, 2))

    participant_ids = fields.One2many(
        'church.mission.participant', 'trip_id', string='Participants')
    support_ids = fields.One2many(
        'church.mission.support', 'trip_id', string='Support')

    participant_count = fields.Integer(
        string='Participant Count', compute='_compute_participant_counts',
        store=True)
    confirmed_participant_count = fields.Integer(
        string='Confirmed Participants',
        compute='_compute_participant_counts', store=True)

    color_index = fields.Integer(
        string='Color', compute='_compute_color_index', store=True)

    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('status_id'):
                vals['status_id'] = self._default_status_id()
            if not vals.get('currency_id'):
                vals['currency_id'] = self.env.company.currency_id.id
        records = super().create(vals_list)
        for record in records:
            if not record.code:
                record.code = self.env['ir.sequence'].next_by_code(
                    'church.mission.trip') or '/'
        return records

    def unlink(self):
        # Event dibuat khusus untuk trip ini (delegation), jadi Event dan
        # baris kalender harus dihapus lebih dulu agar tidak tertinggal
        # sebagai Event/orphan activity.
        events = self.event_id
        self.env['church.activity'].search(
            [('event_id', 'in', events.ids)]).unlink()
        res = super().unlink()
        events.exists().unlink()
        return res

    @api.model
    def _default_status_id(self):
        status = self.env['church.mission.status'].search(
            [('code', '=', 'planned')], limit=1)
        if not status:
            status = self.env['church.mission.status'].search([], limit=1)
        return status.id

    @api.depends('support_ids.amount', 'budget')
    def _compute_support(self):
        for record in self:
            total = sum(record.support_ids.mapped('amount'))
            record.support_total = total
            record.funding_progress = (
                total * 100.0 / record.budget if record.budget else 0.0)

    @api.depends('participant_ids', 'participant_ids.confirmed')
    def _compute_participant_counts(self):
        for record in self:
            record.participant_count = len(record.participant_ids)
            record.confirmed_participant_count = len(
                record.participant_ids.filtered('confirmed'))

    @api.depends('status_id.color')
    def _compute_color_index(self):
        for record in self:
            record.color_index = record.status_id.color or 0
