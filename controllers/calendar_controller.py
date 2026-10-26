# -*- coding: utf-8 -*-
"""JSON endpoints for the church calendar (Flutter mobile API).

Base path: ``/api/v1/mobile/calendar``. Every response is produced through
``controllers/common.py`` and every route is protected by
``controllers/security.py``.

Datetimes are returned as Odoo stores them: naive UTC strings
(``YYYY-MM-DD HH:MM:SS``); the client is responsible for localising them.
"""
from collections import Counter
from datetime import datetime, timedelta

from babel.dates import format_date

from odoo import http
from odoo.exceptions import MissingError, ValidationError
from odoo.fields import Datetime
from odoo.http import request
from odoo.osv import expression

from .common import handle_api_errors, paginated_response, success_response
from .security import require_mobile_api_key

# States hidden from the calendar, mirroring the public /church-calendar page:
# only approved/completed activities are shown, pray requests always are.
CONFIRMED_STATES = ('approved', 'done')

#: ``church.activity`` field -> model of the record the calendar row mirrors.
SOURCE_FIELDS = (
    ('event_id', 'event.event'),
    ('musician_schedule_id', 'church.management.musician.schedule'),
    ('baptism_id', 'church.baptism.registration'),
    ('marriage_id', 'church.marriage.registration'),
    ('care_cell_id', 'church.care.cell'),
    ('pray_request_id', 'church.pray.request'),
    ('sunday_school_session_id', 'church.sunday.school.session'),
)

DEFAULT_LIMIT = 20
MAX_LIMIT = 100
UPCOMING_DEFAULT_LIMIT = 5
UPCOMING_MAX_LIMIT = 50


def _selection(field_name):
    """Return the ``(key, label)`` selections of a ``church.activity`` field."""
    return request.env['church.activity']._fields[field_name].selection or []


def _confirmed_domain():
    """Activities shown on the calendar: pray requests and confirmed states."""
    return expression.OR([
        [('activity_type', '=', 'pray')],
        [('state', '=', False)],
        [('state', 'in', list(CONFIRMED_STATES))],
    ])


def _int_param(value, name, default, minimum=0):
    """Read an integer query parameter, raising ``ValidationError`` if malformed."""
    if value in (None, ''):
        return default
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValidationError("The '%s' parameter must be an integer." % name)
    if number < minimum:
        raise ValidationError(
            "The '%s' parameter must be greater than or equal to %s." % (name, minimum))
    return number


def _datetime_param(value, name):
    """Return ``(datetime, is_date_only)`` for an ISO date or datetime parameter."""
    if not value:
        return None, False
    value = value.strip()
    for fmt, date_only in (('%Y-%m-%d', True),
                           ('%Y-%m-%d %H:%M:%S', False),
                           ('%Y-%m-%dT%H:%M:%S', False)):
        try:
            return datetime.strptime(value, fmt), date_only
        except ValueError:
            continue
    raise ValidationError(
        "The '%s' parameter must use the YYYY-MM-DD or YYYY-MM-DD HH:MM:SS format." % name)


def _range_end(value, date_only):
    """Return the inclusive upper bound for a ``date_to`` filter."""
    if date_only:
        return value + timedelta(days=1) - timedelta(seconds=1)
    return value


def _format_date(value, fmt, fallback):
    """Format ``value`` in the API user's language, falling back to ``fallback``."""
    try:
        return format_date(value, format=fmt, locale=request.env.user.lang or 'en_US')
    except Exception:
        return fallback


def _activity_payload(activity):
    """Serialize one ``church.activity`` record for the mobile client."""
    types = dict(_selection('activity_type'))
    return {
        'id': activity.id,
        'name': activity.name,
        'activity_type': activity.activity_type,
        'activity_type_label': types.get(activity.activity_type, activity.activity_type),
        'start': Datetime.to_string(activity.start) if activity.start else False,
        'stop': Datetime.to_string(activity.stop) if activity.stop else False,
        'state': activity.state or False,
        'color': activity.color,
        'partner': {
            'id': activity.partner_id.id,
            'name': activity.partner_id.name,
        } if activity.partner_id else None,
    }


def _source_payload(activity):
    """Return the record the calendar row mirrors, for drill-down navigation."""
    for field_name, model_name in SOURCE_FIELDS:
        source = activity[field_name]
        if not source:
            continue
        try:
            name = source.display_name
        except Exception:
            # The source model may be readable only through sudo (e.g. events);
            # the ids are still enough for the client to navigate.
            name = False
        return {
            'source_type': activity.activity_type,
            'source_model': model_name,
            'source_id': source.id,
            'source_name': name,
        }
    return None


class ChurchCalendarApi(http.Controller):
    """Read-only calendar endpoints consumed by the Flutter app."""

    def _parse_filters(self, params, default_limit=DEFAULT_LIMIT, max_limit=MAX_LIMIT):
        """Build the search domain and pagination from the query parameters."""
        filters = []

        activity_type = (params.get('type') or '').strip()
        if activity_type:
            if activity_type not in dict(_selection('activity_type')):
                raise ValidationError("Unknown activity type: %s" % activity_type)
            filters.append(('activity_type', '=', activity_type))

        state = (params.get('state') or '').strip()
        if state:
            if state not in dict(_selection('state')):
                raise ValidationError("Unknown activity state: %s" % state)
            filters.append(('state', '=', state))

        date_from, _ = _datetime_param(params.get('date_from'), 'date_from')
        if date_from:
            filters.append(('start', '>=', date_from))

        date_to, date_to_only = _datetime_param(params.get('date_to'), 'date_to')
        if date_to:
            filters.append(('start', '<=', _range_end(date_to, date_to_only)))

        limit = _int_param(params.get('limit'), 'limit', default_limit, minimum=1)
        offset = _int_param(params.get('offset'), 'offset', 0, minimum=0)

        domain = expression.AND([_confirmed_domain(), filters]) if filters else _confirmed_domain()
        return domain, min(limit, max_limit), offset

    @http.route('/api/v1/mobile/calendar/activities', type='http', auth='public',
                methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def calendar_activities(self, **params):
        """Calendar activities, newest first, paginated."""
        domain, limit, offset = self._parse_filters(params)
        Activity = request.env['church.activity']
        total = Activity.search_count(domain)
        activities = Activity.search(
            domain, order='start asc, id asc', limit=limit, offset=offset)
        return paginated_response(
            [_activity_payload(activity) for activity in activities],
            total, limit, offset)

    @http.route('/api/v1/mobile/calendar/activities/<int:activity_id>', type='http',
                auth='public', methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def calendar_activity_detail(self, activity_id, **params):
        """One calendar activity plus the record it mirrors."""
        activity = request.env['church.activity'].browse(activity_id).exists()
        if not activity:
            raise MissingError("Calendar activity %s not found." % activity_id)
        payload = _activity_payload(activity)
        payload['source'] = _source_payload(activity)
        return success_response(payload)

    @http.route('/api/v1/mobile/calendar/agenda', type='http', auth='public',
                methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def calendar_agenda(self, **params):
        """Activities grouped per day with a month roll-up, or grouped per type."""
        group = (params.get('group') or 'day').strip()
        if group not in ('day', 'type'):
            raise ValidationError("The 'group' parameter must be 'day' or 'type'.")

        domain, _limit, _offset = self._parse_filters(params)
        Activity = request.env['church.activity']
        activities = Activity.search(domain, order='start asc, id asc')

        if group == 'type':
            groups = []
            for key, label in _selection('activity_type'):
                items = activities.filtered(lambda act, k=key: act.activity_type == k)
                if items:
                    groups.append({
                        'key': key,
                        'label': label,
                        'count': len(items),
                        'items': [_activity_payload(activity) for activity in items],
                    })
            data = {'group': 'type', 'total': len(activities), 'groups': groups}
        else:
            months = []
            for activity in activities:
                if not activity.start:
                    continue
                month_key = activity.start.strftime('%Y-%m')
                if not months or months[-1]['month'] != month_key:
                    months.append({
                        'month': month_key,
                        'label': _format_date(activity.start, 'MMMM yyyy', month_key),
                        'days': [],
                    })
                day_key = activity.start.strftime('%Y-%m-%d')
                days = months[-1]['days']
                if not days or days[-1]['date'] != day_key:
                    days.append({
                        'date': day_key,
                        'label': _format_date(
                            activity.start, 'EEEE, dd MMMM yyyy', day_key),
                        'items': [],
                    })
                days[-1]['items'].append(_activity_payload(activity))
            data = {'group': 'day', 'total': len(activities), 'months': months}

        return success_response(data)

    @http.route('/api/v1/mobile/calendar/upcoming', type='http', auth='public',
                methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def calendar_upcoming(self, **params):
        """The next activities from now, for the mobile home screen."""
        limit = min(
            _int_param(params.get('limit'), 'limit', UPCOMING_DEFAULT_LIMIT, minimum=1),
            UPCOMING_MAX_LIMIT)
        domain = expression.AND([_confirmed_domain(), [('start', '>=', Datetime.now())]])
        activities = request.env['church.activity'].search(
            domain, order='start asc, id asc', limit=limit)
        return success_response({
            'count': len(activities),
            'items': [_activity_payload(activity) for activity in activities],
        })

    @http.route('/api/v1/mobile/calendar/metrics', type='http', auth='public',
                methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def calendar_metrics(self, **params):
        """Activity counts per type and per month for the dashboard charts."""
        domain, _limit, _offset = self._parse_filters(params)
        activities = request.env['church.activity'].search(domain)

        type_counts = Counter(activity.activity_type for activity in activities)
        month_counts = Counter(
            activity.start.strftime('%Y-%m') for activity in activities if activity.start)

        return success_response({
            'total': len(activities),
            'by_type': [
                {'key': key, 'label': label, 'count': type_counts.get(key, 0)}
                for key, label in _selection('activity_type')
            ],
            'by_month': [
                {'month': month, 'count': count}
                for month, count in sorted(month_counts.items())
            ],
        })
