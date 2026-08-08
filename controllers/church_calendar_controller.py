# -*- coding: utf-8 -*-

from odoo import http, fields
from odoo.http import request


class ChurchCalendar(http.Controller):

    # Activity states considered "confirmed" for public display. Activities
    # without a workflow state (e.g. events, care cells) are always shown.
    CONFIRMED_STATES = ('approved', 'done')

    @http.route('/church-calendar', type='http', auth='public', website=True)
    def church_calendar(self, **kw):
        """Public church calendar page (excludes musician schedules)."""
        Activity = request.env['church.activity'].sudo()

        activities = Activity.search(
            [('activity_type', '!=', 'musician')],
            order='start asc',
        )

        # Only show confirmed activities: hide draft/review/cancelled ones.
        def is_confirmed(act):
            return not act.state or act.state in self.CONFIRMED_STATES

        activities = activities.filtered(is_confirmed)

        # Group upcoming (and ongoing) activities by month for display.
        months = []
        for act in activities:
            if not act.start:
                continue
            month_key = act.start.strftime('%Y-%m')
            month_label = act.start.strftime('%B %Y')
            if not months or months[-1]['key'] != month_key:
                months.append({
                    'key': month_key,
                    'label': month_label,
                    'items': [],
                })
            months[-1]['items'].append(act)

        return request.render('church_management.church_calendar_page', {
            'months': months,
            'total': len(activities),
        })
