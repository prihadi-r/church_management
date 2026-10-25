# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ChurchMissionSupport(models.Model):
    _name = 'church.mission.support'
    _description = 'Mission Support'
    _order = 'date desc, id desc'

    name = fields.Char(string='Reference', readonly=True, copy=False)

    # Donatur memakai res.partner yang sudah ada (Contact).
    partner_id = fields.Many2one(
        'res.partner', string='Donor', required=True,
        ondelete='restrict', index=True)

    date = fields.Date(
        string='Date', required=True, default=fields.Date.context_today)
    amount = fields.Monetary(
        string='Amount', currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')

    # Jenis donasi memakai master yang sudah ada di module ini.
    donation_type_id = fields.Many2one(
        'church.donation.type', string='Donation Type', ondelete='restrict')

    missionary_id = fields.Many2one(
        'church.mission.missionary', string='Missionary',
        ondelete='cascade', index=True)
    trip_id = fields.Many2one(
        'church.mission.trip', string='Mission Trip',
        ondelete='cascade', index=True)

    # Opsional: hubungkan dengan pembayaran akuntansi yang sudah ada.
    payment_id = fields.Many2one(
        'account.payment', string='Accounting Payment', ondelete='set null')

    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('currency_id'):
                vals['currency_id'] = self.env.company.currency_id.id
        records = super().create(vals_list)
        for record in records:
            if not record.name:
                record.name = self.env['ir.sequence'].next_by_code(
                    'church.mission.support') or '/'
            # @api.constrains tidak dijalankan saat create tanpa kedua field
            # tersebut, jadi validasi target dipanggil eksplisit di sini.
            record._check_target()
        return records

    @api.constrains('missionary_id', 'trip_id')
    def _check_target(self):
        for record in self:
            if not record.missionary_id and not record.trip_id:
                raise ValidationError(_(
                    'A mission support must be linked to a missionary or a '
                    'mission trip.'))

    @api.constrains('amount')
    def _check_amount(self):
        for record in self:
            if record.amount <= 0:
                raise ValidationError(
                    _('The support amount must be greater than zero.'))
