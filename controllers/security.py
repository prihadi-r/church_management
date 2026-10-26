# -*- coding: utf-8 -*-
"""API key authentication for the Flutter mobile API.

Every ``/api/v1/mobile/...`` route is protected with
:func:`require_mobile_api_key`, which validates the ``X-Api-Key`` header against
``res.users.apikeys`` and then switches the request environment to the key owner
before the route handler is allowed to run.
"""
import functools
import logging

from odoo.http import request

from .common import error_response

_logger = logging.getLogger(__name__)

API_KEY_HEADER = 'X-Api-Key'
DATABASE_HEADER = 'X-Database'

# Scope checked by ``res.users.apikeys._check_credentials``. Keys generated from
# the web UI are global (scope NULL) and are accepted by the 'rpc' scope.
API_KEY_SCOPE = 'rpc'

# Name of the request attribute holding the user resolved from the API key.
AUTHENTICATED_USER_ATTR = 'mobile_api_user'

# HTTP methods that modify data; they are refused to read-only API users.
WRITE_METHODS = frozenset(['POST', 'PUT', 'PATCH', 'DELETE'])

READ_ONLY_GROUP = 'church_management.group_church_read_only'
WRITE_GROUPS = (
    'church_management.group_church_write_only',
    'church_management.group_church_full_access',
)


def _is_read_only(user):
    """Return whether ``user`` only holds the Church Management read-only role."""
    if not user.has_group(READ_ONLY_GROUP):
        return False
    return not any(user.has_group(group) for group in WRITE_GROUPS)


def require_mobile_api_key(handler):
    """Reject requests that do not carry a valid Odoo API key.

    ``X-Api-Key`` is required and is validated against ``res.users.apikeys``;
    the optional ``X-Database`` header must match the database the request was
    routed to. Once the key is accepted the request environment is switched to
    its owner, so the standard Odoo ACLs apply to everything the handler does.
    Read-only users are refused on data-modifying HTTP methods.
    """
    @functools.wraps(handler)
    def wrapper(*args, **kwargs):
        api_key = (request.httprequest.headers.get(API_KEY_HEADER) or '').strip()
        database = (request.httprequest.headers.get(DATABASE_HEADER) or '').strip()

        if not api_key:
            return error_response(
                401, 'missing_api_key', 'The X-Api-Key header is required.')

        if not request.db:
            return error_response(
                403, 'database_unavailable', 'No database is selected for this request.')

        if database and database != request.db:
            _logger.warning(
                "Mobile API call rejected: X-Database %r does not match %r",
                database, request.db)
            return error_response(
                403, 'database_mismatch', 'The requested database is not available.')

        user_id = request.env['res.users.apikeys'].sudo()._check_credentials(
            scope=API_KEY_SCOPE, key=api_key)
        if not user_id:
            _logger.warning(
                "Mobile API call rejected: invalid API key from %s",
                request.httprequest.remote_addr)
            return error_response(
                401, 'invalid_api_key', 'The provided API key is invalid or expired.')

        setattr(request, AUTHENTICATED_USER_ATTR,
                request.env['res.users'].sudo().browse(user_id))
        request.update_env(user=user_id)

        if request.httprequest.method in WRITE_METHODS and _is_read_only(request.env.user):
            _logger.info(
                "Mobile API call rejected: read-only user %s tried %s %s",
                request.env.user.login, request.httprequest.method,
                request.httprequest.path)
            return error_response(
                403, 'read_only_access',
                'Read-only users are not allowed to modify data through the mobile API.')

        return handler(*args, **kwargs)

    return wrapper


def get_authenticated_user():
    """Return the user authenticated by :func:`require_mobile_api_key`.

    Falls back to the request user when the route is not protected by the
    decorator.
    """
    return getattr(request, AUTHENTICATED_USER_ATTR, None) or request.env.user
