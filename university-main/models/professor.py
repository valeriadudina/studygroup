# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UniversityProfessor(models.Model):
    _name = 'university.professor'
    _description = "Professor entity"

    # professor's properties
    f_name = fields.Char('First name')
    l_name = fields.Char('Last name')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    identity_card = fields.Char('Identity card')
    address = fields.Char('Address')
    birthday = fields.Date('Birthday')
    start_date = fields.Date('Start date')
    email = fields.Char('Email')
    phone = fields.Char('Phone')

    # professor's relationships
    department_id = fields.Many2one(comodel_name='university.department')
    subject_id = fields.Many2one(comodel_name='university.subject')
    classroom_ids = fields.Many2many(comodel_name='university.classroom',
                                     relation='professor_classroom_rel',
                                     column1='f_name',
                                     column2='classroom_name')


    # Get professor names
    # Result : professor window / [Math Informatique Department] Rachid SomeOne
    # @api.multi decorator : @api.many is for multiple records, where you can loop through it etc. It will be the current , https://www.odoo.com/forum/help-1/difference-between-api-one-and-api-multi-in-api-odoo-openerp-68209#
    @api.multi
    def name_get(self):
        result = []
        for professor in self:
            name = '['+ professor.department_id.department_name + '] ' + professor.f_name + ' ' +professor.l_name
            result.append((professor.id, name))

        return result

    # Constraints for `birthday` and `start_date`
    # @api.one to trigger the constrains for each record
    @api.one 
    @api.constrains('birthday', 'start_date')
    def check_date(self):
        if self.birthday >= self.start_date:
            raise ValueError('The Birthday must be inferior of registration date :( .')