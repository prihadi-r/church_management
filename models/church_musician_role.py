# -*- coding: utf-8 -*-
from odoo import models, fields

class ChurchMusicianRole(models.Model):
    _name = 'church.musician.role'
    _description = 'Master: Musician Role'

    # Peran pelayanan musik (Bass, Gitaris, Singer, Worship Leader, Drummer, dll)
    name = fields.Char(string='Role Name', required=True)
