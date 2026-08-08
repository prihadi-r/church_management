# -*- coding: utf-8 -*-
from odoo import models, fields

class ChurchDonationType(models.Model):
    _name = 'church.donation.type'
    _description = 'Master: Donation Type'

    # Klasifikasi jenis donasi (Persembahan Syukur, Perpuluhan, dll)
    name = fields.Char(string='Donation Name', required=True)