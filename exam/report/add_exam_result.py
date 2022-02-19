# See LICENSE file for full copyright and licensing details.

import time

from odoo import api, models


class ReportAddExamResult(models.AbstractModel):
    _name = "report.exam.exam_result_report"
    _description = "Exam result Report"

    @api.model
    def _get_result_detail(self, subject_ids, result):
        """Method to get result data"""
        sub_list = []
        result_data = []
        for sub in subject_ids:
            sub_list.append(sub.id)
        sub_obj = self.env["exam.subject"]
        subject_exam_ids = sub_obj.search(
            [("id", "in", sub_list), ("exam_id", "=", result.id)]
        )
        for subject in subject_exam_ids:
            result_data.append(
                {
                    "subject": subject.subject_id.name or "",
                    "max_mark": subject.maximum_marks or "",
                    "mini_marks": subject.minimum_marks or "",
                    "obt_marks": subject.obtain_marks or "",
                    "reval_marks": subject.marks_reeval or "",
                }
            )
        return result_data

    @api.model
    def _get_report_values(self, docids, data=None):
        """Inherited method to get report values"""
        result_data = self.env['exam.result'].browse(docids)
        return {
            "doc_ids": docids,
            "data": data,
            "doc_model": 'exam.result',
            "docs": result_data,
            "get_result_detail": self._get_result_detail,
            "time": time,
        }
