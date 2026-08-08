# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date

class ChurchBaptismRegistration(models.Model):
    _name = 'church.baptism.registration'
    _description = 'Baptism Registration'
    _order = 'baptism_datetime desc, id desc'

    # Kandidat: selalu terhubung ke res.partner.
    # Field identitas/contact (nama, alamat, telp, email) TIDAK diduplikasi —
    # diambil readonly langsung dari res.partner (related).
    # Catatan: res.partner tidak memiliki field birthdate, sehingga birth_date
    # tetap menjadi field lokal pada baptism (bukan related).
    partner_id = fields.Many2one('res.partner', string='Candidate', required=True, ondelete='restrict')
    name = fields.Char(string='Candidate Name', related='partner_id.name', store=True, index=True)
    birth_date = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    # Orang tua (untuk baptis anak) — juga terhubung ke res.partner
    father_id = fields.Many2one('res.partner', string='Father')
    mother_id = fields.Many2one('res.partner', string='Mother')

    # Kontak diambil dari res.partner (readonly, via related field)
    address = fields.Char(string='Address', related='partner_id.street', readonly=True)
    phone = fields.Char(string='Phone', related='partner_id.phone', readonly=True)
    email = fields.Char(string='Email', related='partner_id.email', readonly=True)

    # Pelaksanaan baptis: SATU field DateTime untuk tanggal + jam
    baptism_datetime = fields.Datetime(string='Baptism Datetime')
    sacrament_type_id = fields.Many2one('church.sacrament.type', string='Sacrament Type')
    pastor_id = fields.Many2one('res.partner', string='Officiating Minister')

    # Status pendaftaran
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')

    # Indeks warna untuk kartu Kanban (dihitung dari status)
    color = fields.Integer(string='Color Index', compute='_compute_color', store=True)

    notes = fields.Text(string='Notes')

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birth_date:
                born = record.birth_date
                record.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            else:
                record.age = 0

    @api.depends('state')
    def _compute_color(self):
        color_map = {
            'draft': 0,
            'review': 3,
            'approved': 4,
            'done': 10,
            'cancel': 1,
        }
        for record in self:
            record.color = color_map.get(record.state, 0)

    def action_submit(self):
        self.state = 'review'

    def action_approve(self):
        self.state = 'approved'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'

    # ===========================================
    # Auto-sync ke kalender kegiatan gereja
    # ===========================================
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            self.env['church.activity']._sync_from_baptism(record)
        return records

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            self.env['church.activity']._sync_from_baptism(record)
        return res

    def unlink(self):
        self.env['church.activity'].search([('baptism_id', 'in', self.ids)]).unlink()
        return super().unlink()