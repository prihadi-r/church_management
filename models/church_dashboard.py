# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class ChurchDashboard(models.Model):
    _name = 'church.dashboard'
    _description = 'Church Management Dashboard'

    name = fields.Char(string='Name', default='Church Management Dashboard')

    # ============ Jemaat ============
    total_members = fields.Integer(string='Total Jemaat', compute='_compute_member_stats')
    # Rincian per tipe anggota dirender sebagai HTML (tabel).
    # Lebih andal daripada computed One2many yang tidak selalu tampil di form.
    member_type_breakdown = fields.Html(string='Jemaat per Tipe Anggota', compute='_compute_member_stats')

    # ============ Baptis ============
    baptism_this_month = fields.Integer(string='Baptisms This Month', compute='_compute_baptism')
    baptism_last_month = fields.Integer(string='Baptisms Last Month', compute='_compute_baptism')
    baptism_queued = fields.Integer(string='Baptisms Queued', compute='_compute_baptism')

    # ============ Pernikahan ============
    marriage_this_month = fields.Integer(string='Marriages This Month', compute='_compute_marriage')
    marriage_last_month = fields.Integer(string='Marriages Last Month', compute='_compute_marriage')
    marriage_queued = fields.Integer(string='Marriages Queued', compute='_compute_marriage')

    # ============ Jadwal Ibadah ============
    worship_this_month = fields.Integer(string='Worship This Month', compute='_compute_worship')
    worship_last_month = fields.Integer(string='Worship Last Month', compute='_compute_worship')
    worship_upcoming = fields.Integer(string='Upcoming Worship', compute='_compute_worship')

    def _month_bounds(self):
        """Return (start_last_month, start_this_month) sebagai datetime."""
        now = datetime.now()
        start_this = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_last = start_this - relativedelta(months=1)
        return start_last, start_this

    def _refresh_stats(self):
        """Hitung ulang seluruh statistik dashboard."""
        self._compute_member_stats()
        self._compute_baptism()
        self._compute_marriage()
        self._compute_worship()

    def read(self, fields=None, load='_classic_read'):
        """Pastikan statistik selalu dihitung ulang saat form dibuka.

        Field statistik adalah non-stored compute TANPA dependensi
        (@api.depends() kosong), sehingga tidak dijamin terhitung otomatis
        ketika record dibaca. Override read() ini memaksa perhitungan ulang
        setiap kali record dibaca oleh form.
        """
        if self:
            self._refresh_stats()
        return super().read(fields, load)

    @api.depends()
    def _compute_member_stats(self):
        Partner = self.env['res.partner']
        for rec in self:
            total = 0
            rows = []
            for mtype in self.env['church.member.type'].search([]):
                count = Partner.search_count([('church_member_type_id', '=', mtype.id)])
                if count:
                    rows.append(
                        '<tr><td>%s</td><td class="text-right">%s</td></tr>'
                        % (mtype.name, count)
                    )
                    total += count
            rec.total_members = total
            rec.member_type_breakdown = (
                '<table class="table table-sm table-bordered mb-0">'
                '<thead><tr><th>Member Type</th>'
                '<th class="text-right">Total</th></tr></thead>'
                '<tbody>%s</tbody>'
                '<tfoot><tr><th>Total Jemaat</th>'
                '<th class="text-right">%s</th></tr></tfoot>'
                '</table>' % (''.join(rows), total)
            )

    @api.depends()
    def _compute_baptism(self):
        start_last, start_this = self._month_bounds()
        for rec in self:
            Bapt = self.env['church.baptism.registration']
            rec.baptism_this_month = Bapt.search_count([
                ('baptism_datetime', '>=', start_this),
            ])
            rec.baptism_last_month = Bapt.search_count([
                ('baptism_datetime', '>=', start_last),
                ('baptism_datetime', '<', start_this),
            ])
            # Masih menunggu proses (draft / under review)
            rec.baptism_queued = Bapt.search_count([('state', 'in', ('draft', 'review'))])

    @api.depends()
    def _compute_marriage(self):
        start_last, start_this = self._month_bounds()
        for rec in self:
            Marr = self.env['church.marriage.registration']
            rec.marriage_this_month = Marr.search_count([
                ('marriage_datetime', '>=', start_this),
            ])
            rec.marriage_last_month = Marr.search_count([
                ('marriage_datetime', '>=', start_last),
                ('marriage_datetime', '<', start_this),
            ])
            # Masih menunggu proses (draft / under review)
            rec.marriage_queued = Marr.search_count([('state', 'in', ('draft', 'review'))])

    @api.depends()
    def _compute_worship(self):
        now = datetime.now()
        start_last, start_this = self._month_bounds()
        for rec in self:
            Event = self.env['event.event']
            rec.worship_this_month = Event.search_count([
                ('date_begin', '>=', start_this),
            ])
            rec.worship_last_month = Event.search_count([
                ('date_begin', '>=', start_last),
                ('date_begin', '<', start_this),
            ])
            # Ibadah yang akan datang
            rec.worship_upcoming = Event.search_count([('date_begin', '>=', now)])
