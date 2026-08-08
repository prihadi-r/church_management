# -*- coding: utf-8 -*-
from odoo import models, fields

class ChurchSacramentType(models.Model):
    _name = 'church.sacrament.type'
    _description = 'Master: Sacrament Type'

    # Klasifikasi jenis sakramen (Baptis, Penyerahan Anak, Pernikahan)
    name = fields.Char(string='Sacrament Name', required=True)