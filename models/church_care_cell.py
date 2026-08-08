# -*- coding: utf-8 -*-
from datetime import date

from odoo import models, fields, api


class ChurchCareCell(models.Model):
    _name = 'church.care.cell'
    _description = 'Master: Care Cell Group'
    _order = 'name'

    # Field untuk nama grup care cell dan relasi ke leader
    name = fields.Char(string='Cell Name', required=True)
    leader_id = fields.Many2one('res.partner', string='Cell Leader')

    # Status care cell (master terpisah, bukan selection field).
    # TIDAK memakai default di level field: default yang melakukan query DB
    # (search ke church.care.cell.status) akan dievaluasi saat schema update
    # (menambah kolom pada tabel yang sudah berisi baris) SEBELUM tabel
    # status dibuat -> UndefinedTable. Default dipindah ke create() override.
    status_id = fields.Many2one(
        'church.care.cell.status',
        string='Status',
    )

    # Sub-class: daftar peserta/anggota care cell (link ke res.partner)
    attendee_ids = fields.One2many(
        'church.care.cell.attendee',
        'care_cell_id',
        string='Attendees',
    )

    # Sub-class: rencana & catatan untuk tiap sesi care cell
    session_ids = fields.One2many(
        'church.care.cell.session',
        'care_cell_id',
        string='Sessions',
    )

    # Periode berlangsungnya care cell (ditampilkan di kalender Care Cell).
    # start_date WAJIB; end_date boleh kosong (masih berjalan / tanpa batas).
    # Care cell disinkronkan ke Church Calendar (church.activity) via
    # create/write/unlink (lihat _sync_from_care_cell di church_activity).
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')

    # Tanggal selesai untuk kalender: fallback ke start_date bila end_date
    # kosong, agar care cell TETAP tampil di Care Cell Calendar.
    calendar_end_date = fields.Date(
        string='Calendar End Date', compute='_compute_calendar_end_date', store=True)

    # Ringkasan untuk tampilan kanban / list / kalender
    attendee_count = fields.Integer(
        string='Attendees Count', compute='_compute_counts', store=True)
    session_count = fields.Integer(
        string='Sessions Count', compute='_compute_counts', store=True)
    next_session_date = fields.Date(
        string='Next Session Date', compute='_compute_next_session_date', store=True)

    # Indeks warna untuk kartu Kanban & Kalender (dihitung dari status).
    # Pola sama persis dengan church.baptism.registration._compute_color.
    color = fields.Integer(string='Color Index', compute='_compute_color', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Set status default = Proposal saat record benar-benar dibuat.

        Default ditempatkan DI SINI (bukan di field) karena default di field
        yang melakukan query DB dievaluasi saat schema update (menambah kolom
        pada tabel yang sudah berisi baris) — sebelum tabel status dibuat —
        dan memicu UndefinedTable.
        """
        for vals in vals_list:
            if not vals.get('status_id'):
                vals['status_id'] = self._default_status_id()
        records = super().create(vals_list)
        # Sinkron ke Church Calendar (church.activity)
        for record in records:
            self.env['church.activity']._sync_from_care_cell(record)
        return records

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            self.env['church.activity']._sync_from_care_cell(record)
        return res

    def unlink(self):
        self.env['church.activity'].search(
            [('care_cell_id', 'in', self.ids)]).unlink()
        return super().unlink()

    @api.model
    def _default_status_id(self):
        """Cari status Proposal (defensif: kembalikan False bila gagal)."""
        try:
            status = self.env['church.care.cell.status'].search(
                [('code', '=', 'proposal')], limit=1)
            return status.id
        except Exception:
            return False

    @api.depends('attendee_ids', 'session_ids')
    def _compute_counts(self):
        for rec in self:
            rec.attendee_count = len(rec.attendee_ids)
            rec.session_count = len(rec.session_ids)

    @api.depends('session_ids.date')
    def _compute_next_session_date(self):
        """Tanggal sesi berikutnya (terdekat >= hari ini);
        bila belum ada, gunakan sesi terakhir yang tercatat."""
        today = date.today()
        for rec in self:
            dates = rec.session_ids.mapped('date')
            if not dates:
                rec.next_session_date = False
                continue
            upcoming = [d for d in dates if d >= today]
            rec.next_session_date = min(upcoming) if upcoming else max(dates)

    @api.depends('start_date', 'end_date')
    def _compute_calendar_end_date(self):
        for rec in self:
            rec.calendar_end_date = rec.end_date or rec.start_date

    @api.depends('status_id.color')
    def _compute_color(self):
        for record in self:
            record.color = record.status_id.color or 0