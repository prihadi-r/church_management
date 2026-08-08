# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class ChurchPray(http.Controller):

    @http.route('/church-pray', type='http', auth='public', website=True)
    def church_pray(self, **kw):
        """Public prayer request form: GET renders the form, POST creates a request."""
        if request.httprequest.method == 'POST':
            return self._submit_pray_request(kw)

        return request.render('church_management.church_pray_page', {})

    def _submit_pray_request(self, kw):
        """Validate and create the prayer request from the public form."""
        title = (kw.get('name_request') or '').strip()
        requester_name = (kw.get('requester_name') or '').strip()
        requester_email = (kw.get('requester_email') or '').strip()
        requester_phone = (kw.get('requester_phone') or '').strip()
        description = (kw.get('description') or '').strip()

        errors = []
        if not title:
            errors.append('Please fill in the prayer request title.')
        if not requester_name:
            errors.append('Please fill in your name.')

        if errors:
            return request.render('church_management.church_pray_page', {
                'errors': errors,
                'form': kw,
            })

        PrayRequest = request.env['church.pray.request'].sudo()

        # Coba kaitkan ke res.partner yang sudah ada (dicari via email), jika ada.
        partner = False
        if requester_email:
            partner = request.env['res.partner'].sudo().search(
                [('email', '=ilike', requester_email)], limit=1)

        values = {
            'name_request': title,
            'requester_name': requester_name,
            'requester_email': requester_email,
            'requester_phone': requester_phone,
            'description': description,
        }
        if partner:
            values['requester_id'] = partner.id

        pray_request = PrayRequest.create(values)

        return request.render('church_management.church_pray_thankyou', {
            'pray_request': pray_request,
        })
