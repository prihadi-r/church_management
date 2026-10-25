# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # Klasifikasi donasi yang masuk ke sistem akuntansi
    church_donation_type_id = fields.Many2one('church.donation.type', string='Donation Type')

    # Dukungan misi (mission support) yang dibayarkan lewat pembayaran ini
    church_mission_support_ids = fields.One2many(
        'church.mission.support', 'payment_id', string='Mission Supports')
