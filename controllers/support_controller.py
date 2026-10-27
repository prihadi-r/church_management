# -*- coding: utf-8 -*-
"""Mission support endpoints for the Flutter mobile API.

Base path: ``/api/v1/mobile/mission/support``. Support entries
(``church.mission.support``) record money a donor gives to a missionary and/or
a mission trip. A record is **collected** once it is linked to an
``account.payment`` (``payment_id``); until then it is a **pending pledge**.

Monetary totals are summed without currency conversion, in the same way as the
web Mission dashboard (multi-currency support is on the backlog of
``task.md``).

Every route composes :func:`controllers.security.require_mobile_api_key` with
:func:`controllers.common.handle_api_errors`; ``POST /pledge`` is refused with
``403 read_only_access`` for read-only API keys.
"""
import json
from datetime import datetime

from odoo import fields, http
from odoo.exceptions import AccessError, ValidationError
from odoo.fields import Datetime
from odoo.http import request

from .common import handle_api_errors, paginated_response, success_response
from .security import require_mobile_api_key

DEFAULT_LIMIT = 20
MAX_LIMIT = 100

_BOOLEAN_VALUES = {
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


def _date_param(value, name):
    """Read a ``YYYY-MM-DD`` query parameter as a date."""
    if not value:
        return None
    try:
        return datetime.strptime(str(value).strip(), '%Y-%m-%d').date()
    except ValueError:
        raise ValidationError(
            "The '%s' parameter must use the YYYY-MM-DD format." % name)


def _collected_param(value):
    """Return ``True`` (collected only), ``False`` (pending only) or ``None``."""
    if value in (None, ''):
        return None
    try:
        return _BOOLEAN_VALUES[str(value).strip().lower()]
    except KeyError:
        raise ValidationError(
            "The 'collected' parameter must be true, false or all.")


def _currency_payload(currency):
    """Serialize a currency reference."""
    if not currency:
        return None
    return {
        'id': currency.id,
        'name': currency.name,
        'symbol': currency.symbol,
    }


def _donation_type_payload(donation_type):
    """Serialize a ``church.donation.type`` reference."""
    if not donation_type:
        return None
    return {'id': donation_type.id, 'name': donation_type.name}


def _payment_payload(payment):
    """Serialize the accounting payment of a collected support, if readable.

    Church users without accounting rights can still see *that* a support was
    paid (`collected`), but not the payment details; in that case the payload
    only carries the id and ``restricted = True``.
    """
    if not payment:
        return None
    try:
        return {
            'id': payment.id,
            'name': payment.name,
            'state': payment.state,
            'date': fields.Date.to_string(payment.date),
            'amount': payment.amount,
            'currency': _currency_payload(payment.currency_id),
            'restricted': False,
        }
    except AccessError:
        return {'id': payment.id, 'name': False, 'state': False,
                'date': False, 'amount': 0.0, 'currency': None,
                'restricted': True}


def _support_payload(support):
    """Serialize one ``church.mission.support`` record."""
    payment = support.payment_id
    missionary = support.missionary_id
    trip = support.trip_id
    return {
        'id': support.id,
        'name': support.name or False,
        'date': fields.Date.to_string(support.date),
        'amount': support.amount,
        'currency': _currency_payload(support.currency_id),
        'donor': {
            'id': support.partner_id.id,
            'name': support.partner_id.name,
        } if support.partner_id else None,
        'donation_type': _donation_type_payload(support.donation_type_id),
        'missionary': {
            'id': missionary.id,
            'code': missionary.code or False,
            'name': missionary.name,
        } if missionary else None,
        'trip': {
            'id': trip.id,
            'code': trip.code or False,
            'name': trip.name,
        } if trip else None,
        'collected': bool(payment),
        'status': 'collected' if payment else 'pending',
        'payment': _payment_payload(payment),
        'notes': support.notes or False,
    }


def _sum(model, domain, measure):
    """Sum ``measure`` of ``model`` over ``domain`` (0.0 when empty)."""
    groups = model._read_group(domain, [], ['%s:sum' % measure])
    return (groups[0][0] if groups else 0.0) or 0.0


def _percent(value, base):
    """Return ``value`` as a percentage of ``base``, rounded to two decimals."""
    return round(value * 100.0 / base, 2) if base else 0.0


def _targets_payload(target, pledged, collected, count):
    """Build one target-attainment block."""
    return {
        'count': count,
        'target': target,
        'pledged': pledged,
        'collected': collected,
        'outstanding': pledged - collected,
        'pledge_progress': _percent(pledged, target),
        'collection_progress': _percent(collected, target),
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


def _amount_body(data):
    """Read the required positive ``amount`` from the request body."""
    value = data.get('amount')
    if value in (None, ''):
        raise ValidationError("The 'amount' field is required.")
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise ValidationError("The 'amount' field must be a number.")
    if amount <= 0:
        raise ValidationError("The 'amount' field must be greater than zero.")
    return amount


def _date_body(data):
    """Read the optional ``date`` (``YYYY-MM-DD``) from the request body."""
    value = data.get('date')
    if value in (None, ''):
        return fields.Date.context_today(request.env.user)
    try:
        return datetime.strptime(str(value).strip(), '%Y-%m-%d').date()
    except ValueError:
        raise ValidationError("The 'date' field must use the YYYY-MM-DD format.")


class ChurchMissionSupportApi(http.Controller):
    """Mission support summary, pledge submission and history endpoints."""

    def _history_domain(self, params):
        """Build the ``church.mission.support`` domain from the query parameters."""
        domain = []

        partner_id = _int_param(params.get('partner_id'), 'partner_id', 0, minimum=1)
        if partner_id:
            domain.append(('partner_id', '=', partner_id))

        missionary_id = _int_param(
            params.get('missionary_id'), 'missionary_id', 0, minimum=1)
        if missionary_id:
            domain.append(('missionary_id', '=', missionary_id))

        trip_id = _int_param(params.get('trip_id'), 'trip_id', 0, minimum=1)
        if trip_id:
            domain.append(('trip_id', '=', trip_id))

        donation_type_id = _int_param(
            params.get('donation_type_id'), 'donation_type_id', 0, minimum=1)
        if donation_type_id:
            domain.append(('donation_type_id', '=', donation_type_id))

        date_from = _date_param(params.get('date_from'), 'date_from')
        if date_from:
            domain.append(('date', '>=', date_from))

        date_to = _date_param(params.get('date_to'), 'date_to')
        if date_to:
            domain.append(('date', '<=', date_to))

        collected = _collected_param(params.get('collected'))
        if collected is not None:
            domain.append(('payment_id', '!=', False) if collected
                          else ('payment_id', '=', False))
        return domain

    @http.route('/api/v1/mobile/mission/support/summary', type='http',
                auth='public', methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def support_summary(self, **params):
        """Funding metrics: pledges, collected amounts and target attainment."""
        Support = request.env['church.mission.support']
        Missionary = request.env['church.mission.missionary']
        Trip = request.env['church.mission.trip']

        collected_domain = [('payment_id', '!=', False)]
        pledged = _sum(Support, [], 'amount')
        collected = _sum(Support, collected_domain, 'amount')
        pledge_count = Support.search_count([])
        collected_count = Support.search_count(collected_domain)

        missionary_target = _sum(Missionary, [('support_target', '>', 0)], 'support_target')
        missionary_pledged = _sum(Support, [('missionary_id', '!=', False)], 'amount')
        missionary_collected = _sum(
            Support, [('missionary_id', '!=', False), ('payment_id', '!=', False)], 'amount')
        missionary_count = Missionary.search_count([('support_target', '>', 0)])

        trip_target = _sum(Trip, [('budget', '>', 0)], 'budget')
        trip_pledged = _sum(Support, [('trip_id', '!=', False)], 'amount')
        trip_collected = _sum(
            Support, [('trip_id', '!=', False), ('payment_id', '!=', False)], 'amount')
        trip_count = Trip.search_count([('budget', '>', 0)])

        by_donation_type = []
        for donation_type, total, count in Support._read_group(
                [], ['donation_type_id'], ['amount:sum', '__count']):
            entry = _donation_type_payload(donation_type) or {
                'id': False, 'name': 'Unspecified'}
            entry.update({'total': total or 0.0, 'count': count})
            by_donation_type.append(entry)
        by_donation_type.sort(key=lambda entry: (-entry['total'], entry['name'] or ''))

        return success_response({
            'generated_at': Datetime.to_string(Datetime.now()),
            'currency': _currency_payload(request.env.company.currency_id),
            'totals': {
                'pledged': pledged,
                'collected': collected,
                'outstanding': pledged - collected,
                'pledge_count': pledge_count,
                'collected_count': collected_count,
                'pending_count': pledge_count - collected_count,
            },
            'targets': {
                'overall': _targets_payload(
                    missionary_target + trip_target,
                    missionary_pledged + trip_pledged,
                    missionary_collected + trip_collected,
                    missionary_count + trip_count),
                'missionaries': _targets_payload(
                    missionary_target, missionary_pledged, missionary_collected,
                    missionary_count),
                'trips': _targets_payload(
                    trip_target, trip_pledged, trip_collected, trip_count),
            },
            'by_donation_type': by_donation_type,
        })

    @http.route('/api/v1/mobile/mission/support/pledge', type='http',
                auth='public', methods=['POST'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def support_pledge(self, **params):
        """Create a pending support pledge (`partner_id`, `amount`, ...)."""
        data = _request_payload()

        partner_id = _int_body(data, 'partner_id', required=True)
        donor = request.env['res.partner'].browse(partner_id).exists()
        if not donor:
            raise ValidationError("The contact %s does not exist." % partner_id)

        amount = _amount_body(data)
        support_date = _date_body(data)

        missionary_id = _int_body(data, 'missionary_id')
        missionary = request.env['church.mission.missionary']
        if missionary_id:
            missionary = missionary.browse(missionary_id).exists()
            if not missionary or not missionary.partner_id.active:
                raise ValidationError(
                    "The missionary %s is not available." % missionary_id)

        trip_id = _int_body(data, 'trip_id')
        trip = request.env['church.mission.trip']
        if trip_id:
            trip = trip.browse(trip_id).exists()
            if not trip or not trip.active:
                raise ValidationError("The mission trip %s is not available." % trip_id)

        if not missionary and not trip:
            raise ValidationError(
                'A support pledge must be linked to a missionary or a mission trip.')

        donation_type_id = _int_body(data, 'donation_type_id')
        if donation_type_id:
            donation_type = request.env['church.donation.type'].browse(
                donation_type_id).exists()
            if not donation_type:
                raise ValidationError(
                    "The donation type %s does not exist." % donation_type_id)

        support = request.env['church.mission.support'].create({
            'partner_id': donor.id,
            'amount': amount,
            'date': support_date,
            'missionary_id': missionary.id or False,
            'trip_id': trip.id or False,
            'donation_type_id': donation_type_id or False,
            'notes': data.get('notes') or False,
        })
        return success_response(_support_payload(support), status=201)

    @http.route('/api/v1/mobile/mission/support/history', type='http',
                auth='public', methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key
    @handle_api_errors
    def support_history(self, **params):
        """Paginated support history (pledges and collected payments)."""
        domain = self._history_domain(params)
        limit = min(
            _int_param(params.get('limit'), 'limit', DEFAULT_LIMIT, minimum=1),
            MAX_LIMIT)
        offset = _int_param(params.get('offset'), 'offset', 0, minimum=0)

        Support = request.env['church.mission.support']
        total = Support.search_count(domain)
        supports = Support.search(
            domain, order='date desc, id desc', limit=limit, offset=offset)
        return paginated_response(
            [_support_payload(support) for support in supports],
            total, limit, offset)
