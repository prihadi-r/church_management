from odoo import models, fields, api
from datetime import datetime, timedelta

class ChurchMusicianSchedule(models.Model):
    _name = 'church.management.musician.schedule'
    _description = 'Church Musician Schedule'

    # 1. Base Fields
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    musician_id = fields.Many2one('res.partner', string='Musician')
    musician_role_id = fields.Many2one('church.musician.role', string='Musician Role', related='musician_id.musician_role_id')
    date = fields.Date(string='Date', required=True)
    
    # Input time fields (e.g. 9.5 = 09:30 AM)
    start_time = fields.Float(string='Start Time (Hours)', help="e.g. 9.5 for 09:30 AM")
    end_time = fields.Float(string='End Time (Hours)', help="e.g. 11.0 for 11:00 AM")

    # 2. Computed Datetime Fields for Calendar View
    start_datetime = fields.Datetime(string='Start Datetime', compute='_compute_datetimes', store=True)
    end_datetime = fields.Datetime(string='End Datetime', compute='_compute_datetimes', store=True)

    @api.depends('musician_id', 'date')
    def _compute_name(self):
        for record in self:
            if record.musician_id and record.date:
                record.name = f"{record.date} - {record.musician_id.name}"
            else:
                record.name = "New Schedule"

    @api.depends('date', 'start_time', 'end_time')
    def _compute_datetimes(self):
        for record in self:
            # Compute start_datetime from date + start_time float
            if record.date and record.start_time is not False:
                start_dt = datetime.combine(record.date, datetime.min.time()) + timedelta(hours=record.start_time)
                record.start_datetime = start_dt
            else:
                record.start_datetime = False

            # Compute end_datetime from date + end_time float
            if record.date and record.end_time is not False:
                end_dt = datetime.combine(record.date, datetime.min.time()) + timedelta(hours=record.end_time)
                record.end_datetime = end_dt
            else:
                record.end_datetime = False

    # ===========================================
    # Auto-sync ke kalender kegiatan gereja
    # ===========================================
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            self.env['church.activity']._sync_from_musician_schedule(record)
        return records

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            self.env['church.activity']._sync_from_musician_schedule(record)
        return res

    def unlink(self):
        self.env['church.activity'].search([('musician_schedule_id', 'in', self.ids)]).unlink()
        return super().unlink()