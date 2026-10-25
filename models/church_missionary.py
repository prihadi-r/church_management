# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ChurchMissionary(models.Model):
    _name = 'church.mission.missionary'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Missionary'
    _order = 'name'

    # Delegasi ke res.partner: nama, telepon, email, alamat, dan foto
    # misionaris memakai field res.partner (tidak diduplikasi).
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True,
        ondelete='cascade', auto_join=True, index=True)

    code = fields.Char(string='Missionary Code', readonly=True, copy=False)

    # Referensi master (bukan selection field)
    field_id = fields.Many2one(
        'church.mission.field', string='Mission Field', ondelete='restrict')
    agency_id = fields.Many2one(
        'church.mission.agency', string='Sending Agency', ondelete='restrict')
    status_id = fields.Many2one(
        'church.missionary.status', string='Status', ondelete='restrict')
    supervisor_id = fields.Many2one(
        'church.mission.missionary', string='Supervisor', ondelete='set null')

    start_date = fields.Date(string='Ministry Start')
    end_date = fields.Date(string='Ministry End')

    currency_id = fields.Many2one('res.currency', string='Currency')
    support_target = fields.Monetary(
        string='Support Target', currency_field='currency_id')
    support_total = fields.Monetary(
        string='Support Received', currency_field='currency_id',
        compute='_compute_support', store=True)
    support_progress = fields.Float(
        string='Support Progress (%)', compute='_compute_support',
        store=True, digits=(5, 2))

    # Perjalanan misi yang dipimpin misionaris ini
    trip_ids = fields.One2many(
        'church.mission.trip', 'leader_id', string='Led Mission Trips')
    support_ids = fields.One2many(
        'church.mission.support', 'missionary_id', string='Support')

    # res.partner.color/active TIDAK didefinisikan ulang di sini agar tidak
    # menutupi field delegasi res.partner.
    color_index = fields.Integer(
        string='Color', compute='_compute_color_index', store=True)

    notes = fields.Text(string='Internal Notes')

    _sql_constraints = [
        ('partner_uniq', 'unique(partner_id)',
         'This contact is already registered as a missionary.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        # Default status/currency dipasang di create (bukan default field)
        # agar tidak melakukan query DB saat schema update.
        for vals in vals_list:
            if not vals.get('status_id'):
                vals['status_id'] = self._default_status_id()
            if not vals.get('currency_id'):
                vals['currency_id'] = self.env.company.currency_id.id
        records = super().create(vals_list)
        for record in records:
            if not record.code:
                record.code = self.env['ir.sequence'].next_by_code(
                    'church.mission.missionary') or '/'
        return records

    @api.model
    def _default_status_id(self):
        status = self.env['church.missionary.status'].search(
            [('code', '=', 'candidate')], limit=1)
        if not status:
            status = self.env['church.missionary.status'].search([], limit=1)
        return status.id

    @api.depends('support_ids.amount', 'support_target')
    def _compute_support(self):
        for record in self:
            total = sum(record.support_ids.mapped('amount'))
            record.support_total = total
            record.support_progress = (
                total * 100.0 / record.support_target
                if record.support_target else 0.0)

    @api.depends('status_id.color')
    def _compute_color_index(self):
        for record in self:
            record.color_index = record.status_id.color or 0
