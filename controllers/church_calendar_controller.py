# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class ChurchCalendar(http.Controller):

    # Activity states considered "confirmed" for public display. Activities
    # without a workflow state (e.g. events, care cells) are always shown.
    CONFIRMED_STATES = ('approved', 'done')

    # Activity types available for public display (musician is excluded).
    ACTIVITY_TYPES = [
        ('event', 'Church Event'),
        ('baptism', 'Baptism'),
        ('marriage', 'Marriage'),
        ('care_cell', 'Care Cell'),
        ('pray', 'Pray Request'),
    ]

    @http.route('/church-calendar', type='http', auth='public', website=True)
    def church_calendar(self, **kw):
        """Public church calendar page (excludes musician schedules)."""
        Activity = request.env['church.activity'].sudo()

        # --- Filters & grouping from query params ---
        active_type = (kw.get('type') or '').strip() or 'all'
        if active_type not in dict(self.ACTIVITY_TYPES):
            active_type = 'all'

        active_group = (kw.get('group') or '').strip() or 'month'
        if active_group not in ('month', 'type'):
            active_group = 'month'

        domain = [('activity_type', '!=', 'musician')]
        if active_type != 'all':
            domain.append(('activity_type', '=', active_type))

        activities = Activity.search(domain, order='start asc')

        # Only show confirmed activities: hide draft/review/cancelled ones.
        # Pray requests have their own statuses and are always shown.
        def is_confirmed(act):
            if act.activity_type == 'pray':
                return True
            return not act.state or act.state in self.CONFIRMED_STATES

        activities = activities.filtered(is_confirmed)

        # --- Grouping ---
        if active_group == 'type':
            groups = []
            months = []
            for key, label in self.ACTIVITY_TYPES:
                items = activities.filtered(lambda a, k=key: a.activity_type == k)
                if items:
                    groups.append({'key': key, 'label': label, 'items': items})
        else:
            groups = []
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
            'groups': groups,
            'types': self.ACTIVITY_TYPES,
            'active_type': active_type,
            'active_group': active_group,
            'total': len(activities),
        })
