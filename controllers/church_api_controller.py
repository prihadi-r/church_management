# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class ChurchApiController(http.Controller):
    
    @http.route('/api/church/events', type='http', auth='public', methods=['GET'], csrf=False)
    def get_events(self, **kwargs):
        """ Fetch semua event gereja yang akan datang beserta roster petugas pelayanannya """
        try:
            events = request.env['event.event'].sudo().search([('event_status', '=', 'upcoming')])
            data = []
            for event in events:
                roster_data = [{
                    'person_name': r.partner_id.name,
                    'role_name': r.role_id.name
                } for r in event.roster_ids]
                
                data.append({
                    'id': event.id,
                    'name': event.name,
                    'date_begin': str(event.date_begin),
                    'roster': roster_data
                })
            
            return request.make_response(
                json.dumps({'status': 200, 'data': data}), 
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({'status': 500, 'error': str(e)}), 
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api/church/sacrament/register', type='http', auth='public', methods=['POST'], csrf=False)
    def register_sacrament(self, **kwargs):
        """ Menerima pendaftaran Sakramen dari Flutter dan memasukkannya ke CRM Odoo """
        try:
            payload = json.loads(request.httprequest.data)
            
            # Buat record CRM Lead baru dari data Flutter
            lead = request.env['crm.lead'].sudo().create({
                'name': f"Registrasi {payload.get('sacrament_name')} - {payload.get('partner_name')}",
                'partner_id': int(payload.get('partner_id')),
                'sacrament_type_id': int(payload.get('sacrament_type_id')),
                'sacrament_state': 'draft'
            })
            
            return request.make_response(
                json.dumps({'status': 201, 'message': 'Pendaftaran berhasil dibuat', 'lead_id': lead.id}), 
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({'status': 500, 'error': str(e)}), 
                headers=[('Content-Type', 'application/json')]
            )