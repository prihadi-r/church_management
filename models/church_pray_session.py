# -*- coding: utf-8 -*-
from odoo import fields, models


class ChurchPraySession(models.Model):
    _name = 'church.pray.session'
    _description = 'Prayer Session'
    _order = 'datetime desc, id desc'

    pray_request_id = fields.Many2one(
        'church.pray.request', string='Prayer Request', required=True, ondelete='cascade')
    name = fields.Char(string='Session Title')
    datetime = fields.Datetime(string='Date & Time', required=True)
    # Orang-orang yang ikut mendoakan (m2m ke contacts / res.partner)
    prayer_ids = fields.Many2many('res.partner', string='Prayers')
    note = fields.Text(string='Notes')
