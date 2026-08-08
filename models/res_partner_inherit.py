# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Keanggotaan gereja
    church_member_type_id = fields.Many2one(
        'church.member.type', string='Church Member Type')
    care_cell_id = fields.Many2one(
        'church.care.cell', string='Care Cell')

    # Data pelayan musik (untuk musician schedule)
    is_musician = fields.Boolean(string='Is Musician')
    musician_role_id = fields.Many2one(
        'church.musician.role', string='Musician Role')

    # TRUE hanya jika tipe anggota = Pastur.
    # Dipakai oleh marriage/baptism untuk menampilkan Officiating Minister
    # hanya pada kontak ber-type Pastur. store=True agar terbaca pada record
    # lama (hooks.py memanggil _compute_is_pastor untuk recompute tersimpan).
    is_pastor = fields.Boolean(
        string='Is Pastor', compute='_compute_is_pastor', store=True)

    @api.depends('church_member_type_id')
    def _compute_is_pastor(self):
        for record in self:
            record.is_pastor = bool(
                record.church_member_type_id
                and record.church_member_type_id.name == 'Pastur')
