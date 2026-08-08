# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ChurchMarriageRegistration(models.Model):
    _name = 'church.marriage.registration'
    _description = 'Marriage Registration'
    _order = 'marriage_datetime desc, id desc'

    # Pasangan pengantin — selalu terhubung ke res.partner
    groom_id = fields.Many2one('res.partner', string='Groom', required=True, ondelete='restrict')
    bride_id = fields.Many2one('res.partner', string='Bride', required=True, ondelete='restrict')
    name = fields.Char(string='Name', compute='_compute_name', store=True)

    # Pelaksanaan nikah: SATU field DateTime untuk tanggal + jam
    marriage_datetime = fields.Datetime(string='Marriage Datetime')
    sacrament_type_id = fields.Many2one('church.sacrament.type', string='Sacrament Type')
    pastor_id = fields.Many2one('res.partner', string='Officiating Minister')
    # Dihitung dari pastor_id: TRUE hanya jika church member type = Pastur.
    # Dipakai agar field Officiating Minister hanya tampil jika si petugas adalah pastur.
    # store=True agar nilai tersimpan di DB dan selalu terbaca pada record yang
    # sudah ada (non-stored compute tidak selalu sampai ke form untuk record lama).
    is_pastor = fields.Boolean(string='Is Pastor', compute='_compute_is_pastor', store=True)

    # Status pendaftaran
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')

    # Indeks warna untuk kartu Kanban / Calendar (dihitung dari status).
    # NON-stored agar perubahan peta warna langsung berlaku pada record
    # yang sudah ada (tanpa perlu recompute tersimpan).
    color = fields.Integer(string='Color Index', compute='_compute_color')

    notes = fields.Text(string='Notes')

    @api.depends('groom_id', 'bride_id')
    def _compute_name(self):
        for record in self:
            if record.groom_id and record.bride_id:
                record.name = f"{record.groom_id.name} & {record.bride_id.name}"
            else:
                record.name = 'Marriage Registration'

    @api.depends('state')
    def _compute_color(self):
        # Indeks warna kanban Odoo: 1=merah, 2=oranye, 3=kuning,
        # 4=biru, 6=hijau — semua status dibedakan warnanya.
        color_map = {
            'draft': 2,
            'review': 3,
            'approved': 4,
            'done': 6,
            'cancel': 1,
        }
        for record in self:
            record.color = color_map.get(record.state, 0)

    @api.depends('pastor_id.is_pastor')
    def _compute_is_pastor(self):
        for record in self:
            record.is_pastor = bool(record.pastor_id and record.pastor_id.is_pastor)

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
            self.env['church.activity']._sync_from_marriage(record)
        return records

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            self.env['church.activity']._sync_from_marriage(record)
        return res

    def unlink(self):
        self.env['church.activity'].search([('marriage_id', 'in', self.ids)]).unlink()
        return super().unlink()
