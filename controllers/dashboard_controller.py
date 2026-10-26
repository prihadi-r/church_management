# -*- coding: utf-8 -*-
"""Consolidated KPI and chart data for the mission dashboard (Flutter mobile API).

Base path: ``/api/v1/mobile/mission/dashboard``. The payload mirrors the eight
graph dashlets of the web Mission dashboard
(``views/church_mission_dashboard_views.xml``) so the app can render the same
charts from pre-aggregated data.

Monetary totals are summed in the company currency; multi-currency support is a
known limitation (see the backlog in ``task.md``).
"""
from odoo import http
from odoo.fields import Datetime
from odoo.http import request
from odoo.osv import expression

from .common import handle_api_errors, success_response
from .security import require_mobile_api_key

#: Trip statuses (``church.mission.status.code``) that count as active.
ACTIVE_TRIP_STATUS_CODES = ('planned', 'ongoing')
#: Missionary status (``church.missionary.status.code``) that counts as in field.
IN_FIELD_STATUS_CODE = 'on_field'


def _active_trip_domain():
    """Trips that are neither completed nor cancelled (unnamed status counts)."""
    return expression.OR([
        [('status_id', '=', False)],
        [('status_id.code', 'in', list(ACTIVE_TRIP_STATUS_CODES))],
    ])


def _group_value(record, field_name):
    """Serialize a many2one group value from ``_read_group``."""
    if not record:
        return {'key': False, 'label': 'Unspecified'}
    value = {'key': record.id, 'label': record.display_name}
    if 'color' in record._fields:
        value['color'] = record.color
    if field_name and field_name in record._fields:
        value['code'] = record[field_name]
    return value


def _count_by(model, domain, groupby):
    """Count ``model`` records grouped by a many2one field, largest first."""
    entries = []
    for record, count in model._read_group(domain, [groupby], ['__count']):
        entry = dict(_group_value(record, 'code'))
        entry['count'] = count
        entries.append(entry)
    entries.sort(key=lambda entry: (-entry['count'], entry['label'] or ''))
    return entries


def _sum_by_relation(model, domain, groupby, measure='amount'):
    """Sum ``measure`` of ``model`` grouped by a many2one field, largest first."""
    entries = []
    for record, total in model._read_group(domain, [groupby], ['%s:sum' % measure]):
        entry = dict(_group_value(record, 'code'))
        entry['total'] = total or 0.0
        entries.append(entry)
    entries.sort(key=lambda entry: (-entry['total'], entry['label'] or ''))
    return entries


def _sum_by_month(model, domain, measure='amount'):
    """Sum ``measure`` of ``model`` per month, oldest first."""
    entries = []
    for month, total in model._read_group(domain, ['date:month'], ['%s:sum' % measure]):
        entries.append({
            'month': month.strftime('%Y-%m'),
            'total': total or 0.0,
        })
    entries.sort(key=lambda entry: entry['month'])
    return entries


def _sum_total(model, domain, measure='amount'):
    """Sum ``measure`` of ``model`` over ``domain``."""
    groups = model._read_group(domain, [], ['%s:sum' % measure])
    return (groups[0][0] if groups else 0.0) or 0.0


class ChurchMissionDashboardApi(http.Controller):
    """Dashboard metrics consumed by the Flutter app."""

    @http.route('/api/v1/mobile/mission/dashboard/metrics', type='http',
                auth='public', methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def mission_dashboard_metrics(self, **params):
        """KPI cards plus the eight dashboard chart series."""
        Trip = request.env['church.mission.trip']
        Missionary = request.env['church.mission.missionary']
        Support = request.env['church.mission.support']
        Participant = request.env['church.mission.participant']

        active_domain = _active_trip_domain()
        now = Datetime.now()
        upcoming_domain = expression.AND([active_domain, [('date_begin', '>=', now)]])
        next_trip = Trip.search(upcoming_domain, order='date_begin asc, id asc', limit=1)

        return success_response({
            'generated_at': Datetime.to_string(now),
            'currency': request.env.company.currency_id.name,
            'kpi': {
                'active_trips': Trip.search_count(active_domain),
                'missionaries_in_field': Missionary.search_count(
                    [('status_id.code', '=', IN_FIELD_STATUS_CODE)]),
                'total_support_raised': _sum_total(Support, []),
                'upcoming_departures': Trip.search_count(upcoming_domain),
                'next_departure': (
                    Datetime.to_string(next_trip.date_begin) if next_trip else False),
            },
            'charts': {
                'trips_by_status': _count_by(Trip, [], 'status_id'),
                'trips_by_type': _count_by(Trip, [], 'type_id'),
                'trips_by_field': _count_by(Trip, [], 'field_id'),
                'missionaries_by_status': _count_by(Missionary, [], 'status_id'),
                'participants_by_role': _count_by(Participant, [], 'role_id'),
                'support_by_month': _sum_by_month(Support, []),
                'support_by_missionary': _sum_by_relation(Support, [], 'missionary_id'),
                'support_by_donation_type': _sum_by_relation(
                    Support, [], 'donation_type_id'),
            },
        })
