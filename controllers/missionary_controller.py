# -*- coding: utf-8 -*-
"""Missionary endpoints for the Flutter mobile API.

Base path: ``/api/v1/mobile/missionaries``. Missionaries delegate to
``res.partner``, so every payload exposes the contact data (name, phone, email,
address, photo) next to the mission fields (field, agency, status, support).

``GET /<id>/avatar`` streams the cached partner image from
``res.partner.image_1920`` / ``image_256`` and advertises ``ETag`` and
``Last-Modified``, so the app can revalidate with ``If-None-Match`` /
``If-Modified-Since`` and get ``304 Not Modified`` instead of the bytes.

Every route composes :func:`controllers.security.require_mobile_api_key` with
:func:`controllers.common.handle_api_errors`.
"""
import base64
from datetime import timezone
from email.utils import format_datetime, parsedate_to_datetime

from odoo import fields, http
from odoo.exceptions import MissingError, ValidationError
from odoo.fields import Datetime
from odoo.http import request

from .common import (
    handle_api_errors,
    paginated_response,
    success_response,
)
from .security import require_mobile_api_key

DEFAULT_LIMIT = 20
MAX_LIMIT = 100

#: ``size`` query parameter -> ``res.partner`` image field.
AVATAR_FIELDS = {
    '1920': 'image_1920',
    '256': 'image_256',
}

_ACTIVE_VALUES = {
    '1': True, 'true': True, 'yes': True,
    '0': False, 'false': False, 'no': False,
    'all': None,
}


def _dt(value):
    """Serialize a datetime the way Odoo stores it (naive UTC string)."""
    return Datetime.to_string(value) if value else False


def _active_param(value):
    """Return ``True`` (active only), ``False`` (archived only) or ``None`` (all)."""
    if value in (None, ''):
        return True
    try:
        return _ACTIVE_VALUES[str(value).strip().lower()]
    except KeyError:
        raise ValidationError(
            "The 'active' parameter must be true, false or all.")


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


def _active_domain(active):
    """Domain term on the delegated ``res.partner.active`` flag."""
    if active is None:
        return []
    return [('partner_id.active', '=', active)]


def _master_payload(record):
    """Serialize a mission master record (field, status, ...)."""
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


def _currency_payload(currency):
    """Serialize a currency reference."""
    if not currency:
        return None
    return {
        'id': currency.id,
        'name': currency.name,
        'symbol': currency.symbol,
    }


def _address_payload(partner):
    """Serialize the postal address of a contact."""
    country = partner.country_id
    state = partner.state_id
    return {
        'street': partner.street or False,
        'street2': partner.street2 or False,
        'city': partner.city or False,
        'zip': partner.zip or False,
        'state': {'id': state.id, 'name': state.name} if state else None,
        'country': {
            'id': country.id,
            'code': country.code,
            'name': country.name,
        } if country else None,
    }


def _contact_payload(partner, with_address=False):
    """Serialize the contact details shared by partners, missionaries and agencies."""
    if not partner:
        return None
    payload = {
        'id': partner.id,
        'name': partner.name,
        'phone': partner.phone or False,
        'mobile': partner.mobile or False,
        'email': partner.email or False,
        'image_url': '/web/image/res.partner/%s/image_256' % partner.id,
    }
    if 'website' in partner._fields:
        payload['website'] = partner.website or False
    if with_address:
        payload['address'] = _address_payload(partner)
    return payload


def _missionary_brief(missionary):
    """Serialize a missionary reference (supervisor, leader, ...)."""
    if not missionary:
        return None
    return {
        'id': missionary.id,
        'code': missionary.code or False,
        'name': missionary.name,
    }


def _agency_brief(agency):
    """Serialize a mission agency reference."""
    if not agency:
        return None
    return {
        'id': agency.id,
        'code': agency.code or False,
        'name': agency.name,
    }


def _avatar_url(missionary, size):
    """Return the API avatar route for ``missionary`` at ``size``."""
    return '/api/v1/mobile/missionaries/%s/avatar?size=%s' % (missionary.id, size)


def _missionary_payload(missionary):
    """Serialize one missionary for the directory list."""
    partner = missionary.partner_id
    return {
        'id': missionary.id,
        'code': missionary.code or False,
        'name': partner.name,
        'partner_id': partner.id,
        'active': partner.active,
        'phone': partner.phone or False,
        'mobile': partner.mobile or False,
        'email': partner.email or False,
        'image_url': '/web/image/res.partner/%s/image_256' % partner.id,
        'avatar_url': _avatar_url(missionary, '256'),
        'status': _master_payload(missionary.status_id),
        'field': _master_payload(missionary.field_id),
        'agency': _agency_brief(missionary.agency_id),
        'start_date': fields.Date.to_string(missionary.start_date),
        'end_date': fields.Date.to_string(missionary.end_date),
        'currency': _currency_payload(missionary.currency_id),
        'support_target': missionary.support_target,
        'support_total': missionary.support_total,
        'support_progress': missionary.support_progress,
        'color': missionary.color_index,
    }


def _missionary_detail_payload(missionary):
    """Serialize one missionary with contact, agency, trips and support data."""
    payload = _missionary_payload(missionary)
    agency = missionary.agency_id
    support_ids = missionary.support_ids
    payload.update({
        'contact': _contact_payload(missionary.partner_id, with_address=True),
        'agency': {
            'id': agency.id,
            'code': agency.code or False,
            'name': agency.name,
            'contact': _contact_payload(agency.partner_id),
        } if agency else None,
        'supervisor': _missionary_brief(missionary.supervisor_id),
        'notes': missionary.notes or False,
        'trips': [{
            'id': trip.id,
            'code': trip.code or False,
            'name': trip.name,
            'date_begin': _dt(trip.date_begin),
            'date_end': _dt(trip.date_end),
            'status': _master_payload(trip.status_id),
        } for trip in missionary.trip_ids],
        'trip_count': len(missionary.trip_ids),
        'support': {
            'total': missionary.support_total,
            'count': len(support_ids),
            'last_date': fields.Date.to_string(
                max(support_ids.mapped('date')) if support_ids else False),
        },
        'avatar_urls': {
            size: _avatar_url(missionary, size) for size in sorted(AVATAR_FIELDS)
        },
    })
    return payload


def _missionary_or_404(missionary_id):
    """Return the missionary with ``missionary_id`` or raise ``MissingError`` (404)."""
    missionary = request.env['church.mission.missionary'].browse(missionary_id).exists()
    if not missionary:
        raise MissingError("Missionary %s not found." % missionary_id)
    return missionary


def _image_mimetype(data):
    """Guess the image MIME type from its magic bytes."""
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    if data.startswith(b'\xff\xd8\xff'):
        return 'image/jpeg'
    if data.startswith((b'GIF87a', b'GIF89a')):
        return 'image/gif'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'image/webp'
    return 'application/octet-stream'


def _etag(partner, size):
    """Build a weak ``ETag`` from the contact's last write and the image size."""
    stamp = 0
    if partner.write_date:
        stamp = int(partner.write_date.replace(tzinfo=timezone.utc).timestamp())
    return 'W/"%s-%s"' % (stamp, size)


def _is_not_modified(etag, last_modified):
    """Evaluate the ``If-None-Match`` / ``If-Modified-Since`` request headers."""
    headers = request.httprequest.headers

    if_none_match = (headers.get('If-None-Match') or '').strip()
    if if_none_match:
        def _normalize(tag):
            return tag.replace('W/', '').strip().strip('"')
        return any(
            _normalize(tag) == _normalize(etag)
            for tag in if_none_match.split(',') if tag.strip())

    if_modified_since = headers.get('If-Modified-Since')
    if if_modified_since and last_modified:
        try:
            since = parsedate_to_datetime(if_modified_since)
        except (TypeError, ValueError):
            return False
        if since.tzinfo is None:
            since = since.replace(tzinfo=timezone.utc)
        modified = last_modified.replace(tzinfo=timezone.utc, microsecond=0)
        return modified <= since
    return False


class ChurchMissionaryApi(http.Controller):
    """Missionary directory, profile and avatar endpoints."""

    @http.route('/api/v1/mobile/missionaries', type='http', auth='public',
                methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def missionary_list(self, **params):
        """Paginated missionaries with their contact details and support progress."""
        active = _active_param(params.get('active'))
        limit = min(
            _int_param(params.get('limit'), 'limit', DEFAULT_LIMIT, minimum=1),
            MAX_LIMIT)
        offset = _int_param(params.get('offset'), 'offset', 0, minimum=0)

        domain = _active_domain(active)

        status_id = _int_param(params.get('status_id'), 'status_id', 0, minimum=1)
        if status_id:
            domain.append(('status_id', '=', status_id))

        field_id = _int_param(params.get('field_id'), 'field_id', 0, minimum=1)
        if field_id:
            domain.append(('field_id', '=', field_id))

        agency_id = _int_param(params.get('agency_id'), 'agency_id', 0, minimum=1)
        if agency_id:
            domain.append(('agency_id', '=', agency_id))

        Missionary = request.env['church.mission.missionary'].with_context(
            active_test=False)
        total = Missionary.search_count(domain)
        missionaries = Missionary.search(
            domain, order='name asc, id asc', limit=limit, offset=offset)
        return paginated_response(
            [_missionary_payload(missionary) for missionary in missionaries],
            total, limit, offset)

    @http.route('/api/v1/mobile/missionaries/<int:missionary_id>', type='http',
                auth='public', methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def missionary_detail(self, missionary_id, **params):
        """One missionary with contact, agency, field, trips and total support."""
        return success_response(
            _missionary_detail_payload(_missionary_or_404(missionary_id)))

    @http.route('/api/v1/mobile/missionaries/<int:missionary_id>/avatar',
                type='http', auth='public', methods=['GET'], csrf=False,
                save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def missionary_avatar(self, missionary_id, **params):
        """Stream the missionary photo, honouring ``If-None-Match`` / ``If-Modified-Since``."""
        missionary = _missionary_or_404(missionary_id)
        size = str(params.get('size') or '256').strip()
        if size not in AVATAR_FIELDS:
            raise ValidationError(
                "The 'size' parameter must be one of: %s."
                % ', '.join(sorted(AVATAR_FIELDS)))

        partner = missionary.partner_id
        image_base64 = partner[AVATAR_FIELDS[size]]
        if not image_base64:
            raise MissingError("Missionary %s has no photo." % missionary_id)

        etag = _etag(partner, size)
        last_modified = partner.write_date
        headers = [('ETag', etag), ('Cache-Control', 'private, max-age=86400')]
        if last_modified:
            headers.append((
                'Last-Modified',
                format_datetime(
                    last_modified.replace(tzinfo=timezone.utc), usegmt=True)))

        if _is_not_modified(etag, last_modified):
            return request.make_response('', status=304, headers=headers)

        image = base64.b64decode(image_base64)
        headers.extend([
            ('Content-Type', _image_mimetype(image)),
            ('Content-Length', str(len(image))),
        ])
        return request.make_response(image, status=200, headers=headers)
