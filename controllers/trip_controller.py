# -*- coding: utf-8 -*-
"""Mission trip endpoints for the Flutter mobile API.

Base path: ``/api/v1/mobile/mission/trips``. A mission trip *is* an
``event.event`` (``church.mission.trip`` delegates to it), so the payloads also
expose the inherited event fields: name, dates, venue and seats.

Every route composes :func:`controllers.security.require_mobile_api_key` with
:func:`controllers.common.handle_api_errors`; write routes additionally rely on
the Odoo ACLs of the authenticated user, so the read-only role is refused by
the API-key decorator before the handler runs.

Datetimes are returned as Odoo stores them: naive UTC strings
(``YYYY-MM-DD HH:MM:SS``).
"""
import json
from datetime import datetime, timedelta

from odoo import fields, http
from odoo.exceptions import MissingError, ValidationError
from odoo.fields import Datetime
from odoo.http import request
from odoo.osv import expression

from .common import handle_api_errors, paginated_response, success_response
from .security import require_mobile_api_key

DEFAULT_LIMIT = 20
MAX_LIMIT = 100

#: ``confirmed`` query parameter values for the participants list.
_CONFIRMED_VALUES = {
    '1': True, 'true': True, 'yes': True,
    '0': False, 'false': False, 'no': False,
    'all': None,
}


def _dt(value):
    """Serialize a datetime the way Odoo stores it (naive UTC string)."""
    return Datetime.to_string(value) if value else False


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
    value = str(value).strip()
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
    """Return the inclusive upper bound for a ``date_end`` filter."""
    if date_only:
        return value + timedelta(days=1) - timedelta(seconds=1)
    return value


def _confirmed_param(value):
    """Return ``True`` (only confirmed), ``False`` (only pending) or ``None``."""
    if value in (None, ''):
        return True
    try:
        return _CONFIRMED_VALUES[str(value).strip().lower()]
    except KeyError:
        raise ValidationError(
            "The 'confirmed' parameter must be true, false or all.")


def _master_payload(record):
    """Serialize a mission master record (type, field, status, role, agency)."""
    if not record:
        return None
    payload = {
        'id': record.id,
        'name': record.name,
        'code': record.code or False,
    }
    if 'color' in record._fields:
        payload['color'] = record.color
    if 'is_closed' in record._fields:
        payload['is_closed'] = record.is_closed
    return payload


def _contact_payload(partner):
    """Serialize the contact details shared by partners, missionaries and agencies."""
    if not partner:
        return None
    return {
        'id': partner.id,
        'name': partner.name,
        'phone': partner.phone or False,
        'mobile': partner.mobile or False,
        'email': partner.email or False,
        'image_url': '/web/image/res.partner/%s/image_128' % partner.id,
    }


def _currency_payload(currency):
    """Serialize a currency reference."""
    if not currency:
        return None
    return {
        'id': currency.id,
        'name': currency.name,
        'symbol': currency.symbol,
    }


def _venue_payload(address):
    """Serialize the venue (``event.event.address_id``) of a trip."""
    if not address:
        return None
    country = address.country_id
    return {
        'id': address.id,
        'name': address.display_name,
        'city': address.city or False,
        'country': {
            'id': country.id,
            'code': country.code,
            'name': country.name,
        } if country else None,
    }


def _seats_payload(trip):
    """Serialize the event seat configuration of a trip."""
    return {
        'limited': trip.seats_limited,
        'max': trip.seats_max,
        'taken': trip.seats_taken,
        'available': trip.seats_available,
    }


def _trip_payload(trip):
    """Serialize one mission trip for the list screen."""
    return {
        'id': trip.id,
        'code': trip.code or False,
        'name': trip.name,
        'event_id': trip.event_id.id,
        'type': _master_payload(trip.type_id),
        'field': _master_payload(trip.field_id),
        'agency': _master_payload(trip.agency_id),
        'status': _master_payload(trip.status_id),
        'leader': _contact_payload(trip.leader_id.partner_id),
        'date_begin': _dt(trip.date_begin),
        'date_end': _dt(trip.date_end),
        'date_tz': trip.date_tz or False,
        'is_ongoing': trip.is_ongoing,
        'is_finished': trip.is_finished,
        'venue': _venue_payload(trip.address_id),
        'budget': trip.budget,
        'currency': _currency_payload(trip.currency_id),
        'support_total': trip.support_total,
        'funding_progress': trip.funding_progress,
        'participant_count': trip.participant_count,
        'confirmed_participant_count': trip.confirmed_participant_count,
        'seats': _seats_payload(trip),
        'color': trip.color_index,
    }


def _trip_detail_payload(trip):
    """Serialize one mission trip with the inherited event fields and counts."""
    payload = _trip_payload(trip)
    payload.update({
        'description': trip.description or False,
        'note': trip.note or False,
        'notes': trip.notes or False,
        'event_status': trip.event_status,
        'organizer': _contact_payload(trip.organizer_id),
        'responsible': {
            'id': trip.user_id.id,
            'name': trip.user_id.name,
        } if trip.user_id else None,
        'tags': [{'id': tag.id, 'name': tag.name} for tag in trip.tag_ids],
        'support': {
            'total': trip.support_total,
            'count': len(trip.support_ids),
        },
        'participants': {
            'total': trip.participant_count,
            'confirmed': trip.confirmed_participant_count,
            'pending': trip.participant_count - trip.confirmed_participant_count,
        },
    })
    return payload


def _participant_payload(participant):
    """Serialize one ``church.mission.participant`` record."""
    return {
        'id': participant.id,
        'partner_id': participant.partner_id.id,
        'name': participant.name,
        'phone': participant.phone or False,
        'mobile': participant.mobile or False,
        'email': participant.email or False,
        'image_url': '/web/image/res.partner/%s/image_128' % participant.partner_id.id,
        'role': _master_payload(participant.role_id),
        'confirmed': participant.confirmed,
        'registration_date': fields.Date.to_string(participant.registration_date),
        'notes': participant.notes or False,
        'color': participant.color_index,
    }


def _request_payload():
    """Return the JSON (or form-encoded) body of a write request as a dict."""
    raw = request.httprequest.get_data(cache=True, as_text=True) or ''
    if not raw.strip():
        return dict(request.params)
    try:
        data = json.loads(raw)
    except ValueError:
        raise ValidationError('The request body must be valid JSON.')
    if not isinstance(data, dict):
        raise ValidationError('The request body must be a JSON object.')
    return data


def _int_body(data, name, required=False):
    """Read an integer id from the request body."""
    value = data.get(name)
    if value in (None, ''):
        if required:
            raise ValidationError("The '%s' field is required." % name)
        return False
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValidationError("The '%s' field must be an integer." % name)


def _trip_or_404(trip_id):
    """Return the trip with ``trip_id`` or raise ``MissingError`` (404)."""
    trip = request.env['church.mission.trip'].browse(trip_id).exists()
    if not trip:
        raise MissingError("Mission trip %s not found." % trip_id)
    return trip


def _seats_used(trip):
    """Seats consumed by a trip: mission participants plus event registrations."""
    return max(trip.participant_count, trip.seats_taken)


class ChurchMissionTripApi(http.Controller):
    """Mission trip list, detail, participants and registration endpoints."""

    def _parse_filters(self, params):
        """Build the search domain and pagination from the query parameters."""
        filters = []

        field_id = _int_param(params.get('field_id'), 'field_id', 0, minimum=1)
        if field_id:
            filters.append(('field_id', '=', field_id))

        status_id = _int_param(params.get('status_id'), 'status_id', 0, minimum=1)
        if status_id:
            filters.append(('status_id', '=', status_id))

        # ``date_begin`` / ``date_end`` select the trips that overlap the
        # requested window, not only those starting or ending inside it.
        date_begin, _ = _datetime_param(params.get('date_begin'), 'date_begin')
        if date_begin:
            filters.append(('date_end', '>=', date_begin))

        date_end, date_end_only = _datetime_param(params.get('date_end'), 'date_end')
        if date_end:
            filters.append(('date_begin', '<=', _range_end(date_end, date_end_only)))

        limit = min(
            _int_param(params.get('limit'), 'limit', DEFAULT_LIMIT, minimum=1),
            MAX_LIMIT)
        offset = _int_param(params.get('offset'), 'offset', 0, minimum=0)
        return filters, limit, offset

    @http.route('/api/v1/mobile/mission/trips', type='http', auth='public',
                methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def trip_list(self, **params):
        """Paginated mission trips with status, field, dates and funding progress."""
        filters, limit, offset = self._parse_filters(params)
        Trip = request.env['church.mission.trip']
        total = Trip.search_count(filters)
        trips = Trip.search(filters, limit=limit, offset=offset)
        return paginated_response(
            [_trip_payload(trip) for trip in trips], total, limit, offset)

    @http.route('/api/v1/mobile/mission/trips/<int:trip_id>', type='http',
                auth='public', methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def trip_detail(self, trip_id, **params):
        """One mission trip with its inherited event fields and counts."""
        return success_response(_trip_detail_payload(_trip_or_404(trip_id)))

    @http.route('/api/v1/mobile/mission/trips/<int:trip_id>/participants',
                type='http', auth='public', methods=['GET'], csrf=False,
                save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def trip_participants(self, trip_id, **params):
        """Participants of a trip (confirmed only unless ``confirmed=false|all``)."""
        trip = _trip_or_404(trip_id)
        confirmed = _confirmed_param(params.get('confirmed'))
        limit = min(
            _int_param(params.get('limit'), 'limit', DEFAULT_LIMIT, minimum=1),
            MAX_LIMIT)
        offset = _int_param(params.get('offset'), 'offset', 0, minimum=0)

        domain = [('trip_id', '=', trip.id)]
        if confirmed is not None:
            domain = expression.AND([domain, [('confirmed', '=', confirmed)]])

        Participant = request.env['church.mission.participant']
        total = Participant.search_count(domain)
        participants = Participant.search(
            domain, order='name asc, id asc', limit=limit, offset=offset)
        return paginated_response(
            [_participant_payload(participant) for participant in participants],
            total, limit, offset)

    @http.route('/api/v1/mobile/mission/trips/<int:trip_id>/register',
                type='http', auth='public', methods=['POST'], csrf=False,
                save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def trip_register(self, trip_id, **params):
        """Register a contact on a trip (``partner_id``, ``role_id``, ``notes``)."""
        trip = _trip_or_404(trip_id)
        data = _request_payload()

        partner_id = _int_body(data, 'partner_id', required=True)
        partner = request.env['res.partner'].browse(partner_id).exists()
        if not partner:
            raise ValidationError(
                "The contact %s does not exist." % partner_id)

        role_id = _int_body(data, 'role_id')
        if role_id:
            role = request.env['church.mission.role'].browse(role_id).exists()
            if not role or not role.active:
                raise ValidationError(
                    "The participant role %s is not available." % role_id)

        Participant = request.env['church.mission.participant']
        if Participant.search_count(
                [('trip_id', '=', trip.id), ('partner_id', '=', partner.id)]):
            raise ValidationError(
                'This contact is already registered on this mission trip.')

        now = Datetime.now()
        if trip.date_end and trip.date_end < now:
            raise ValidationError(
                'The mission trip "%s" has already ended.' % trip.name)

        used = _seats_used(trip)
        if trip.seats_limited and trip.seats_max and used >= trip.seats_max:
            raise ValidationError(
                'The mission trip "%s" is full (%s of %s seats taken).'
                % (trip.name, used, trip.seats_max))

        participant = Participant.create({
            'partner_id': partner.id,
            'trip_id': trip.id,
            'role_id': role_id or False,
            'notes': data.get('notes') or False,
            'confirmed': False,
        })
        return success_response(_participant_payload(participant), status=201)
