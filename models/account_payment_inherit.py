# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # Klasifikasi donasi yang masuk ke sistem akuntansi
    church_donation_type_id = fields.Many2one('church.donation.type', string='Donation Type')