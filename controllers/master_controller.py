# -*- coding: utf-8 -*-
"""Mission master-data endpoints for the Flutter mobile API.

Base path: ``/api/v1/mobile/mission/master``. These routes expose the
configuration records the app needs to build pickers and filters: mission
types, geographic fields, trip/missionary statuses and participant roles.
All of them are read-only and protected by
:func:`controllers.security.require_mobile_api_key`.

The ``active`` query parameter accepts ``true`` (default: only active
records), ``false`` (only archived records) or ``all`` (both).
"""
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from .common import handle_api_errors, paginated_response, success_response
from .security import require_mobile_api_key

DEFAULT_LIMIT = 50
MAX_LIMIT = 200

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


def _master_model(model_name, active):
    """Return ``model_name``, also reading archived rows when ``active`` allows it."""
    model = request.env[model_name]
    return model if active is True else model.with_context(active_test=False)


def _active_domain(active):
    """Domain term that keeps only archived rows when ``active`` is ``False``."""
    return [('active', '=', False)] if active is False else []


def _base_payload(record):
    """Serialize the fields shared by every mission master record."""
    return {
        'id': record.id,
        'name': record.name,
        'code': record.code or False,
        'sequence': record.sequence,
        'color': record.color,
        'active': record.active,
    }


def _type_payload(mission_type):
    """Serialize one ``church.mission.type`` record."""
    payload = _base_payload(mission_type)
    payload['description'] = mission_type.description or False
    return payload


def _field_payload(mission_field):
    """Serialize one ``church.mission.field`` record."""
    payload = _base_payload(mission_field)
    country = mission_field.country_id
    payload['country'] = {
        'id': country.id,
        'code': country.code,
        'name': country.name,
    } if country else None
    parent = mission_field.parent_id
    payload['parent'] = {'id': parent.id, 'name': parent.name} if parent else None
    payload['description'] = mission_field.description or False
    return payload


def _status_payload(status):
    """Serialize one trip or missionary status record."""
    payload = _base_payload(status)
    payload['is_closed'] = status.is_closed
    return payload


class ChurchMissionMasterApi(http.Controller):
    """Read-only master data consumed by the Flutter app."""

    @http.route('/api/v1/mobile/mission/master/types', type='http', auth='public',
                methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def master_types(self, **params):
        """Mission types (``church.mission.type``), ordered by sequence."""
        active = _active_param(params.get('active'))
        mission_types = _master_model(
            'church.mission.type', active).search(_active_domain(active))
        items = [_type_payload(mission_type) for mission_type in mission_types]
        return success_response({'total': len(items), 'items': items})

    @http.route('/api/v1/mobile/mission/master/fields', type='http', auth='public',
                methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def master_fields(self, **params):
        """Mission fields / regions (``church.mission.field``), paginated."""
        active = _active_param(params.get('active'))
        limit = min(
            _int_param(params.get('limit'), 'limit', DEFAULT_LIMIT, minimum=1),
            MAX_LIMIT)
        offset = _int_param(params.get('offset'), 'offset', 0, minimum=0)

        MissionField = _master_model('church.mission.field', active)
        domain = _active_domain(active)
        total = MissionField.search_count(domain)
        fields = MissionField.search(domain, limit=limit, offset=offset)
        return paginated_response(
            [_field_payload(mission_field) for mission_field in fields],
            total, limit, offset)

    @http.route('/api/v1/mobile/mission/master/statuses', type='http', auth='public',
                methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def master_statuses(self, **params):
        """Trip statuses and missionary statuses in a single payload."""
        active = _active_param(params.get('active'))
        domain = _active_domain(active)
        trip_statuses = _master_model(
            'church.mission.status', active).search(domain)
        missionary_statuses = _master_model(
            'church.missionary.status', active).search(domain)
        return success_response({
            'trip_statuses': [_status_payload(status) for status in trip_statuses],
            'missionary_statuses': [
                _status_payload(status) for status in missionary_statuses],
        })

    @http.route('/api/v1/mobile/mission/master/roles', type='http', auth='public',
                methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def master_roles(self, **params):
        """Participant roles (``church.mission.role``), ordered by sequence."""
        active = _active_param(params.get('active'))
        roles = _master_model('church.mission.role', active).search(
            _active_domain(active))
        items = [_base_payload(role) for role in roles]
        return success_response({'total': len(items), 'items': items})
