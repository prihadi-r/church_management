# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ChurchPrayRequest(models.Model):
    _name = 'church.pray.request'
    _description = 'Prayer Request'
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Request Reference', readonly=True, copy=False)
    requester_id = fields.Many2one('res.partner', string='Requester', ondelete='restrict')
    # Kontak pemohon disimpan sebagai teks agar publik bisa mengisi tanpa harus
    # membuat res.partner (public user tidak punya akses create ke res.partner).
    requester_name = fields.Char(string='Requester Name')
    requester_email = fields.Char(string='Requester Email')
    requester_phone = fields.Char(string='Requester Phone')

    name_request = fields.Char(string='Request Title', required=True)
    description = fields.Text(string='Prayer Request Details')

    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('answered', 'Answered'),
        ('closed', 'Closed'),
    ], string='Status', default='new')

    color = fields.Integer(string='Color Index', compute='_compute_color', store=True)

    # Sesi-sesi doa untuk permohonan ini (o2m)
    session_ids = fields.One2many('church.pray.session', 'pray_request_id', string='Prayer Sessions')

    @api.depends('state')
    def _compute_color(self):
        color_map = {
            'new': 0,
            'in_progress': 3,
            'answered': 10,
            'closed': 1,
        }
        for record in self:
            record.color = color_map.get(record.state, 0)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if not record.name:
                record.name = self.env['ir.sequence'].next_by_code('church.pray.request')
            self.env['church.activity']._sync_from_pray_request(record)
        return records

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            self.env['church.activity']._sync_from_pray_request(record)
        return res

    def unlink(self):
        self.env['church.activity'].search([('pray_request_id', 'in', self.ids)]).unlink()
        return super().unlink()

    def action_start(self):
        self.state = 'in_progress'

    def action_answered(self):
        self.state = 'answered'

    def action_close(self):
        self.state = 'closed'

    def action_reopen(self):
        self.state = 'in_progress'
