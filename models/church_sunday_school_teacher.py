# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ChurchSundaySchoolTeacher(models.Model):
    _name = 'church.sunday.school.teacher'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Sunday School Teacher'
    _order = 'name'

    # Delegasi ke res.partner: data kontak guru (nama, telepon, email,
    # alamat) dipakai langsung dari kontak gereja.
    partner_id = fields.Many2one(
        'res.partner', string='Contact',
        required=True, ondelete='cascade', auto_join=True, index=True)

    since_date = fields.Date(string='Serving Since')

    # Sub-class: penugasan guru pada kelas (peran diatur per penugasan)
    assignment_ids = fields.One2many(
        'church.sunday.school.class.teacher', 'teacher_id',
        string='Class Assignments')
    class_count = fields.Integer(
        string='Classes', compute='_compute_class_count', store=True)

    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('partner_uniq', 'unique(partner_id)',
         'This contact is already registered as a Sunday school teacher.'),
    ]

    @api.depends('assignment_ids')
    def _compute_class_count(self):
        for record in self:
            record.class_count = len(record.assignment_ids)
