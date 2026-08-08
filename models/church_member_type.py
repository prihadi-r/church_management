# -*- coding: utf-8 -*-
from odoo import models, fields

class ChurchMemberType(models.Model):
    _name = 'church.member.type'
    _description = 'Master: Church Member Type'

    # Field untuk nama jenis jemaat (Simpatisan, Jemaat Tetap, dll)
    name = fields.Char(string='Member Type', required=True)