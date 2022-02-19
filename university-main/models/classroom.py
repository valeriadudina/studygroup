# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UniversityClassroom(models.Model):
    _name = 'university.classroom'
    _description = "Classroom entity"

    # department's properties
    classroom_name = fields.Char(string='name')
    code = fields.Char()

    # classroom's relationships
    student_ids = fields.One2many(comodel_name='university.student', inverse_name='classroom_id')
    professor_ids = fields.Many2many(comodel_name='university.professor',
                                     relation='classroom_professor_rel',
                                     column1='classroom_name',
                                     column2='f_name')
    subject_ids = fields.Many2many(comodel_name='university.subject',
                                   relation='classroom_subject_rel',
                                   column1='classroom_name',
                                   column2='subject_name')

    # Computed fields
    num_prof = fields.Integer(string='Number of professors', compute='comp_prof')
    num_sub = fields.Integer(string='Number of subjects', compute='comp_sub')
    num_stud = fields.Integer(string='Number of student', compute='comp_stu')

    # Compute professors
    def comp_prof(self):
        self.num_prof = len(self.professor_ids)

    # Compute subjects
    def comp_sub(self):
        self.num_sub = len(self.subject_ids)

    # Compute students
    def comp_stu(self):
        self.num_stud = len(self.student_ids)

    # add constraints to nbr subject per classroom
    # @api.onchange
    @api.onchange('subject_ids')
    def check_number_of_subject(self):
        if len(self.subject_ids) > 3:
            return{'warning': {'title': 'warning', 'message': 'The number of subjects must be less then 3 per classroom :('}}
