# -*- coding: utf-8 -*-
from odoo import api, models, fields


class ChurchMissionAgency(models.Model):
    _name = 'church.mission.agency'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Mission Agency'
    _order = 'name'

    # Delegasi ke res.partner: agency adalah sebuah organisasi/kontak, jadi
    # nama, alamat, telepon, email, dan website memakai field res.partner.
    # Catatan: res.partner.color/active TIDAK didefinisikan ulang di sini agar
    # tidak menutupi (shadow) field delegasi dari res.partner.
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True,
        ondelete='cascade', auto_join=True, index=True)

    code = fields.Char(string='Agency Code', copy=False)

    field_ids = fields.Many2many(
        'church.mission.field',
        'church_mission_agency_field_rel', 'agency_id', 'field_id',
        string='Mission Fields')

    missionary_ids = fields.One2many(
        'church.mission.missionary', 'agency_id', string='Missionaries')
    trip_ids = fields.One2many(
        'church.mission.trip', 'agency_id', string='Mission Trips')

    missionary_count = fields.Integer(
        string='Missionary Count', compute='_compute_counts', store=True)
    trip_count = fields.Integer(
        string='Mission Trip Count', compute='_compute_counts', store=True)

    notes = fields.Text(string='Internal Notes')

    @api.depends('missionary_ids', 'trip_ids')
    def _compute_counts(self):
        for record in self:
            record.missionary_count = len(record.missionary_ids)
            record.trip_count = len(record.trip_ids)

    @api.model_create_multi
    def create(self, vals_list):
        # Agency adalah organisasi: partner yang dibuat otomatis harus
        # bertipe company agar tampil sebagai perusahaan di Contacts.
        for vals in vals_list:
            if not vals.get('partner_id'):
                vals.setdefault('is_company', True)
        return super().create(vals_list)
