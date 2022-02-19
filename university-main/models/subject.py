# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UniversitySubject(models.Model):
    _name = 'university.subject'
    _description = "Subject entity"

    # department's properties
    subject_name = fields.Char(string='name')
    code = fields.Char()

    # subject's relationships
    department_id = fields.Many2one(comodel_name='university.department')
    student_id = fields.Many2one(comodel_name='university.student')
    professor_ids = fields.One2many(comodel_name='university.professor', inverse_name='subject_id')
    classroom_ids = fields.Many2many(comodel_name='university.classroom',
                                     relation='subject_classroom_rel',
                                     column1='subject_name',
                                     column2='classroom_name')


