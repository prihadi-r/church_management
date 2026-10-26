# -*- coding: utf-8 -*-
"""Shared JSON envelope and error handling for the Flutter mobile API.

Routes are expected to compose the decorators in this order::

    @http.route('/api/v1/mobile/...', type='http', auth='public',
                methods=['GET'], csrf=False, save_session=False)
    @require_mobile_api_key          # controllers/security.py
    @handle_api_errors               # this module
    def endpoint(self, **kwargs):
        ...
        return success_response(payload)

Authentication errors are produced by :func:`require_mobile_api_key` itself, so
only errors raised by the endpoint body are converted here.
"""
import functools
import logging

from werkzeug.exceptions import HTTPException

from odoo import exceptions
from odoo.http import request

_logger = logging.getLogger(__name__)


def success_response(data=None, status=200):
    """Wrap ``data`` into the standard success envelope."""
    return request.make_json_response(
        {'success': True, 'data': data}, status=status)


def error_response(status, code, message):
    """Build the standard error envelope.

    ``message`` is shown to the mobile client and must therefore stay
    user-friendly; tracebacks and SQL details belong in the server log.
    """
    return request.make_json_response({
        'success': False,
        'error': {'code': code, 'message': message},
    }, status=status)


def paginated_response(items, total, limit, offset, status=200):
    """Wrap a page of ``items`` together with the pagination metadata."""
    return success_response({
        'items': items,
        'total': total,
        'limit': limit,
        'offset': offset,
    }, status=status)


def _user_error_details(exc):
    """Map an Odoo user-facing exception to ``(status, code)``."""
    if isinstance(exc, exceptions.ValidationError):
        return 400, 'validation_error'
    if isinstance(exc, exceptions.AccessError):
        return 403, 'access_error'
    if isinstance(exc, exceptions.AccessDenied):
        return 403, 'access_denied'
    if isinstance(exc, exceptions.MissingError):
        return 404, 'not_found'
    return 400, 'user_error'


def handle_api_errors(handler):
    """Turn exceptions raised by an endpoint into the standard error envelope."""
    @functools.wraps(handler)
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except exceptions.UserError as exc:
            status, code = _user_error_details(exc)
            _logger.info("Mobile API error [%s]: %s", code, exc)
            return error_response(status, code, str(exc) or code)
        except HTTPException as exc:
            return error_response(
                exc.code or 500, 'http_error', exc.description or 'HTTP error')
        except Exception:
            _logger.exception("Mobile API unexpected error")
            return error_response(
                500, 'internal_error', 'An unexpected server error occurred.')

    return wrapper
