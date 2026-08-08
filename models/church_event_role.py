# -*- coding: utf-8 -*-
from odoo import models, fields

class ChurchEventRole(models.Model):
    _name = 'church.event.role'
    _description = 'Master: Event Role'

    # Peran pelayanan di gereja (Musisi, Pastor, WL, Usher)
    name = fields.Char(string='Role Name', required=True)