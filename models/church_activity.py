# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta

class ChurchActivity(models.Model):
    _name = 'church.activity'
    _description = 'Church Activity Calendar'
    _order = 'start desc, id desc'

    # ===========================================
    # Fields Umum
    # ===========================================
    name = fields.Char(string='Title', required=True)
    activity_type = fields.Selection([
        ('event', 'Church Event'),
        ('musician', 'Musician Schedule'),
        ('baptism', 'Baptism'),
        ('marriage', 'Marriage'),
        ('care_cell', 'Care Cell'),
        ('pray', 'Pray Request'),
        ('sunday_school', 'Sunday School'),
    ], string='Activity Type', required=True)

    start = fields.Datetime(string='Start')
    stop = fields.Datetime(string='End')
    color = fields.Integer(string='Color')
    partner_id = fields.Many2one('res.partner', string='Contact')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled'),
    ], string='Status')

    # Referensi ke record sumber (untuk navigasi ke detail)
    event_id = fields.Many2one('event.event', string='Church Event', ondelete='cascade')
    musician_schedule_id = fields.Many2one('church.management.musician.schedule', string='Musician Schedule', ondelete='cascade')
    baptism_id = fields.Many2one('church.baptism.registration', string='Baptism Registration', ondelete='cascade')
    marriage_id = fields.Many2one('church.marriage.registration', string='Marriage Registration', ondelete='cascade')
    care_cell_id = fields.Many2one('church.care.cell', string='Care Cell', ondelete='cascade')
    pray_request_id = fields.Many2one('church.pray.request', string='Pray Request', ondelete='cascade')
    sunday_school_session_id = fields.Many2one(
        'church.sunday.school.session', string='Sunday School Session',
        ondelete='cascade')

    # ===========================================
    # Generate Kalender dari seluruh kegiatan
    # ===========================================
    @api.model
    def regenerate(self):
        """Regenerate semua baris kalender dari seluruh kegiatan gereja."""
        self.search([]).unlink()
        Activity = self.env['church.activity']

        # 1. Event Gereja (event.event)
        for event in self.env['event.event'].search([]):
            if not event.date_begin or not event.active:
                continue
            Activity.create({
                'name': event.name,
                'activity_type': 'event',
                'start': event.date_begin,
                'stop': event.date_end,
                'color': 0,
                'event_id': event.id,
            })

        # 2. Jadwal Musisi (church.management.musician.schedule)
        for ms in self.env['church.management.musician.schedule'].search([]):
            if not ms.start_datetime:
                continue
            Activity.create({
                'name': ms.name or 'Musician Schedule',
                'activity_type': 'musician',
                'start': ms.start_datetime,
                'stop': ms.end_datetime,
                'color': 1,
                'partner_id': ms.musician_id.id,
                'musician_schedule_id': ms.id,
            })

        # 3. Pendaftaran Baptis (church.baptism.registration)
        for bapt in self.env['church.baptism.registration'].search([]):
            if not bapt.baptism_datetime:
                continue
            Activity.create({
                'name': f"{bapt.name} - Baptis",
                'activity_type': 'baptism',
                'start': bapt.baptism_datetime,
                'stop': bapt.baptism_datetime + timedelta(hours=1),
                'color': 2,
                'partner_id': bapt.partner_id.id,
                'baptism_id': bapt.id,
                'state': bapt.state,
            })

        # 4. Pendaftaran Pernikahan (church.marriage.registration)
        for marriage in self.env['church.marriage.registration'].search([]):
            if not marriage.marriage_datetime:
                continue
            Activity.create({
                'name': f"{marriage.name} - Pernikahan",
                'activity_type': 'marriage',
                'start': marriage.marriage_datetime,
                'stop': marriage.marriage_datetime + timedelta(hours=2),
                'color': 5,
                'partner_id': marriage.groom_id.id,
                'marriage_id': marriage.id,
                'state': marriage.state,
            })

        # 5. Care Cell (church.care.cell)
        for cell in self.env['church.care.cell'].search([]):
            if not cell.start_date:
                continue
            stop_date = cell.end_date or cell.start_date
            Activity.create({
                'name': cell.name,
                'activity_type': 'care_cell',
                'start': fields.Datetime.to_datetime(cell.start_date),
                'stop': fields.Datetime.to_datetime(stop_date),
                'color': cell.color or 0,
                'partner_id': cell.leader_id.id,
                'care_cell_id': cell.id,
            })

        # 6. Permohonan Doa (church.pray.request)
        for pray in self.env['church.pray.request'].search([]):
            if not pray.create_date:
                continue
            Activity.create({
                'name': f"{pray.name_request} - Doa",
                'activity_type': 'pray',
                'start': pray.create_date,
                'color': 9,
                'partner_id': pray.requester_id.id,
                'pray_request_id': pray.id,
            })

        # 7. Sesi Sekolah Minggu (church.sunday.school.session)
        for session in self.env['church.sunday.school.session'].search([]):
            if not session.start_datetime:
                continue
            Activity.create({
                'name': session.name,
                'activity_type': 'sunday_school',
                'start': session.start_datetime,
                'stop': session.calendar_stop,
                'color': session.color or 0,
                'partner_id': session.teacher_id.partner_id.id,
                'sunday_school_session_id': session.id,
            })

    # ===========================================
    # Auto-sync: sinkron satu record sumber
    # ===========================================
    @api.model
    def _sync_from_baptism(self, bapt):
        """Buat/perbarui baris kalender untuk satu pendaftaran baptis."""
        activity = self.search([('baptism_id', '=', bapt.id)], limit=1)
        if not bapt.baptism_datetime:
            if activity:
                activity.unlink()
            return
        vals = {
            'name': f"{bapt.name} - Baptis",
            'activity_type': 'baptism',
            'start': bapt.baptism_datetime,
            'stop': bapt.baptism_datetime + timedelta(hours=1),
            'color': 2,
            'partner_id': bapt.partner_id.id,
            'baptism_id': bapt.id,
            'state': bapt.state,
        }
        if activity:
            activity.write(vals)
        else:
            self.create(vals)

    @api.model
    def _sync_from_musician_schedule(self, ms):
        """Buat/perbarui baris kalender untuk satu jadwal musisi."""
        activity = self.search([('musician_schedule_id', '=', ms.id)], limit=1)
        if not ms.start_datetime:
            if activity:
                activity.unlink()
            return
        vals = {
            'name': ms.name or 'Musician Schedule',
            'activity_type': 'musician',
            'start': ms.start_datetime,
            'stop': ms.end_datetime,
            'color': 1,
            'partner_id': ms.musician_id.id,
            'musician_schedule_id': ms.id,
        }
        if activity:
            activity.write(vals)
        else:
            self.create(vals)

    @api.model
    def _sync_from_event(self, event):
        """Buat/perbarui baris kalender untuk satu event gereja."""
        activity = self.search([('event_id', '=', event.id)], limit=1)
        if not event.date_begin or not event.active:
            if activity:
                activity.unlink()
            return
        vals = {
            'name': event.name,
            'activity_type': 'event',
            'start': event.date_begin,
            'stop': event.date_end,
            'color': 0,
            'event_id': event.id,
        }
        if activity:
            activity.write(vals)
        else:
            self.create(vals)

    @api.model
    def _sync_from_marriage(self, marriage):
        """Buat/perbarui baris kalender untuk satu pendaftaran pernikahan."""
        activity = self.search([('marriage_id', '=', marriage.id)], limit=1)
        if not marriage.marriage_datetime:
            if activity:
                activity.unlink()
            return
        vals = {
            'name': f"{marriage.name} - Pernikahan",
            'activity_type': 'marriage',
            'start': marriage.marriage_datetime,
            'stop': marriage.marriage_datetime + timedelta(hours=2),
            'color': 5,
            'partner_id': marriage.groom_id.id,
            'marriage_id': marriage.id,
            'state': marriage.state,
        }
        if activity:
            activity.write(vals)
        else:
            self.create(vals)

    @api.model
    def _sync_from_pray_request(self, pray):
        """Buat/perbarui baris kalender untuk satu permohonan doa."""
        activity = self.search([('pray_request_id', '=', pray.id)], limit=1)
        if not pray.create_date:
            if activity:
                activity.unlink()
            return
        vals = {
            'name': f"{pray.name_request} - Doa",
            'activity_type': 'pray',
            'start': pray.create_date,
            'color': 9,
            'partner_id': pray.requester_id.id,
            'pray_request_id': pray.id,
        }
        if activity:
            activity.write(vals)
        else:
            self.create(vals)

    @api.model
    def _sync_from_care_cell(self, cell):
        """Buat/perbarui baris kalender untuk satu care cell.

        stop selalu diisi (fallback ke start_date) agar care cell dengan
        end_date kosong tetap muncul di Church Calendar.
        """
        activity = self.search([('care_cell_id', '=', cell.id)], limit=1)
        if not cell.start_date:
            if activity:
                activity.unlink()
            return
        stop_date = cell.end_date or cell.start_date
        vals = {
            'name': cell.name,
            'activity_type': 'care_cell',
            'start': fields.Datetime.to_datetime(cell.start_date),
            'stop': fields.Datetime.to_datetime(stop_date),
            'color': cell.color or 0,
            'partner_id': cell.leader_id.id,
            'care_cell_id': cell.id,
        }
        if activity:
            activity.write(vals)
        else:
            self.create(vals)

    @api.model
    def _sync_from_sunday_school_session(self, session):
        """Buat/perbarui baris kalender untuk satu sesi sekolah minggu."""
        activity = self.search(
            [('sunday_school_session_id', '=', session.id)], limit=1)
        if not session.start_datetime:
            if activity:
                activity.unlink()
            return
        vals = {
            'name': session.name,
            'activity_type': 'sunday_school',
            'start': session.start_datetime,
            'stop': session.calendar_stop,
            'color': session.color or 0,
            'partner_id': session.teacher_id.partner_id.id,
            'sunday_school_session_id': session.id,
        }
        if activity:
            activity.write(vals)
        else:
            self.create(vals)

    def action_refresh(self):
        """Tombol untuk memuat ulang kalender."""
        self.regenerate()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Church Calendar',
            'res_model': 'church.activity',
            'view_mode': 'calendar,list,form',
            'target': 'current',
        }
