# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
import datetime
from odoo.exceptions import Warning
from odoo.exceptions import UserError


class KeralaAcademy(models.Model):
    _name = "kerala.academy"
    _rec_name = "student_id"

    academy_name = fields.Char(string="Academy Name")
    student_id = fields.Many2one('res.partner', string="Student Name")
    course_enrolled = fields.Many2one('course.master', string="Courser Name")
    total_fees = fields.Float(string="Total Fees", compute="_compute_total_fees", store=True)
    fees_paid = fields.Float(string="Fees Paid")
    remaining_fees_to_pay = fields.Float(string="Remaining Fees To pay", compute="_calculate_remaining_fees",
                                         store=True)
    is_fully_paid = fields.Boolean(string="Is Fully Paid?", compute="_calculate_remaining_fees", store=True)
    certificate_number = fields.Char(string="Certificate Number")

    @api.model
    def create(self, vals):
        vals['certificate_number'] = self.env['ir.sequence'].next_by_code('kerala.academy')
        return super(KeralaAcademy, self).create(vals)

    @api.depends('course_enrolled')
    def _compute_total_fees(self):
        for i in self:
            i.total_fees = i.course_enrolled.course_fee

    @api.depends('fees_paid')
    def _calculate_remaining_fees(self):
        for j in self:
            j.remaining_fees_to_pay = j.total_fees - j.fees_paid
            if j.remaining_fees_to_pay == 0.0 and j.fees_paid != 0.0:
                j.is_fully_paid = True
            else:
                j.is_fully_paid = False

    def print_certificate(self):
        if self.is_fully_paid:
            return self.env.ref('academy.academy_certificate_print_badge').report_action(self)
        else:
            raise UserError(_('You Can not print certifcate before they fees fully paid!'))

    def get_today_date(self):
        today = datetime.datetime.today().strftime('%d/%m/%y')
        return today


class CourseMaster(models.Model):
    _name = "course.master"
    _rec_name = "course_name"

    course_name = fields.Char(string="Name")
    course_fee = fields.Float(string="Course Fees")
