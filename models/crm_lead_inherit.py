# -*- coding: utf-8 -*-
from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Pendaftaran Sakramen diintegrasikan ke dalam CRM Pipeline
    sacrament_type_id = fields.Many2one('church.sacrament.type', string='Sacrament Type')
    
    # Penggunaan Selection field hanya diizinkan untuk state/status
    sacrament_state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled')
    ], string='Sacrament Status', default='draft')