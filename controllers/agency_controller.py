# -*- coding: utf-8 -*-
"""Mission agency directory for the Flutter mobile API.

Base path: ``/api/v1/mobile/missionaries/agencies``. Agencies delegate to
``res.partner`` (a company contact), so the payload carries the organisation
contact data, the mission fields the agency works in, and how many **active**
missionaries and trips it currently has.

Every route composes :func:`controllers.security.require_mobile_api_key` with
:func:`controllers.common.handle_api_errors`.
"""
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from .common import handle_api_errors, paginated_response
from .security import require_mobile_api_key

DEFAULT_LIMIT = 20
MAX_LIMIT = 100

_ACTIVE_VALUES = {
    '1': True, 'true': True, 'yes': True,
    '0': False, 'false': False, 'no': False,
    'all': None,
}


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


def _active_missionary_count(agency):
    """Count the agency's missionaries whose contact is still active."""
    return len(agency.missionary_ids.filtered(lambda m: m.partner_id.active))


def _agency_payload(agency):
    """Serialize one ``church.mission.agency`` record with its counts."""
    partner = agency.partner_id
    return {
        'id': agency.id,
        'code': agency.code or False,
        'name': partner.name,
        'partner_id': partner.id,
        'active': partner.active,
        'phone': partner.phone or False,
        'mobile': partner.mobile or False,
        'email': partner.email or False,
        'website': partner.website or False,
        'image_url': '/web/image/res.partner/%s/image_256' % partner.id,
        'address': _address_payload(partner),
        'mission_fields': [
            {'id': mission_field.id, 'name': mission_field.name}
            for mission_field in agency.field_ids
        ],
        'missionary_count': _active_missionary_count(agency),
        'trip_count': agency.trip_count,
        'notes': agency.notes or False,
    }


class ChurchMissionAgencyApi(http.Controller):
    """Mission agency directory consumed by the Flutter app."""

    @http.route('/api/v1/mobile/missionaries/agencies', type='http',
                auth='public', methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def agency_list(self, **params):
        """Paginated agencies with contact data and their active missionary count."""
        active = _active_param(params.get('active'))
        limit = min(
            _int_param(params.get('limit'), 'limit', DEFAULT_LIMIT, minimum=1),
            MAX_LIMIT)
        offset = _int_param(params.get('offset'), 'offset', 0, minimum=0)

        domain = [] if active is None else [('partner_id.active', '=', active)]

        field_id = _int_param(params.get('field_id'), 'field_id', 0, minimum=1)
        if field_id:
            domain.append(('field_ids', 'in', [field_id]))

        Agency = request.env['church.mission.agency'].with_context(active_test=False)
        total = Agency.search_count(domain)
        agencies = Agency.search(
            domain, order='name asc, id asc', limit=limit, offset=offset)
        return paginated_response(
            [_agency_payload(agency) for agency in agencies], total, limit, offset)
