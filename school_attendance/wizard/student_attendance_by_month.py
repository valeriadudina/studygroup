# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StudentAttendanceByMonth(models.TransientModel):
    """Defining Student Attendance By Month."""

    _name = "student.attendance.by.month"
    _description = "Student Monthly Attendance Report"

    month = fields.Many2one("academic.month", help="Select academic month")
    year = fields.Many2one("academic.year", help="Select academic year")
    attendance_type = fields.Selection(
        [("daily", "FullDay"), ("lecture", "Lecture Wise")],
        "Type",
        help="Select attendance type",
    )

    @api.model
    def default_get(self, fields):
        """Overriding DefaultGet."""
        res = super(StudentAttendanceByMonth, self).default_get(fields)
        students_rec = self.env["student.student"].browse(
            self._context.get("active_id")
        )
        if students_rec.state == "draft":
            raise ValidationError(
                _(
                    """
                You can not print report for student in unconfirm state!"""
                )
            )
        return res

    def print_report(self):
        """ This method prints report
        @param self : Object Pointer
        @param cr : Database Cursor
        @param uid : Current Logged in User
        @param ids : Current Records
        @param context : standard Dictionary
        @return : printed report
        """
        stud_search_rec = self.env["student.student"].search(
            [
                ("id", "=", self.env.context.get("active_id")),
                ("state", "=", "done"),
            ]
        )
        daily_attend = self.env["daily.attendance"]
        for rec in self:
            if not daily_attend.search([
                ("standard_id", "=", stud_search_rec.standard_id.id),
                ("date", ">=", rec.month.date_start),
                ("date", "<=", rec.month.date_stop)], limit =1):
                raise ValidationError(
                    _(
                        """
        There is no data of attendance for student in selected month or year!
        """
                    )
                )
        data = self.read([])[0]
        if data.get("year"):
            data["year"] = self.year.name
        data.update({"stud_ids": self.env.context.get("active_ids")})
        datas = {
            "ids": [],
            "model": "student.student",
            "type": "ir.actions.report.xml",
            "form": data,
        }
        return self.env.ref(
            "school_attendance.attendace_month_report"
        ).report_action([], data=datas)
