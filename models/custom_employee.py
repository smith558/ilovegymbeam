# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
# for working with Excel files
from xlrd import open_workbook
import base64, magic


class CustomEmployee(models.Model):
    _inherit = 'hr.employee'

    i_love_gb = fields.Boolean(string='I Love GB')

    salary = fields.Integer(string='Salary')
    tax = fields.Integer(string='Tax')
    total_salary = fields.Integer(string='Total Salary', compute='_compute_total_salary', store=True)
    special_phone = fields.Char(string='Special Phone', default='0901123456')
    employee_contacts = fields.Binary(string='Employee Contacts', attachment=True)
    # a unique employee tracking number
    employee_number = fields.Char(string='Employee Number', required=True, tracking=True)

    @api.depends('salary', 'tax')
    def _compute_total_salary(self):
        for record in self:
            record.total_salary = record.salary + record.tax

    @api.model
    def create(self, vals):
        if 'employee_contacts' in vals:
            self._check_excel_file(vals['employee_contacts'])
        # ensures uniqueness of `employee_number` across system
        if 'employee_number' in vals:
            # Check against employees (active and archived)
            employee_count = self.env['hr.employee'].with_context(active_test=False).search_count(
                [('employee_number', '=', vals['employee_number'])])

            # Check against applicants (active and archived)
            applicant_count = self.env['hr.applicant'].with_context(active_test=False).search_count(
                [('employee_number', '=', vals['employee_number'])])

            if employee_count or applicant_count:
                raise exceptions.ValidationError('Employee number must be unique across employees and applicants!')
        return super(CustomEmployee, self).create(vals)

    def write(self, vals):
        # to deal with updates only (creation dealt with via the "default" parameter)
        if 'special_phone' in vals and not vals['special_phone']:
            vals['special_phone'] = '0901123456'
        # check if file is Excel
        if 'employee_contacts' in vals:
            self._check_excel_file(vals['employee_contacts'])
        # ensures uniqueness of `employee_number` across system
        if 'employee_number' in vals:
            for record in self:
                # Check against employees (active and archived)
                employee_count = self.env['hr.employee'].with_context(active_test=False).search_count(
                    [('employee_number', '=', vals['employee_number']), ('id', '!=', record.id)])

                # Check against other applicants (active and archived)
                applicant_count = self.env['hr.applicant'].with_context(active_test=False).search_count(
                    [('employee_number', '=', vals['employee_number'])])

                if employee_count or applicant_count:
                    raise exceptions.ValidationError('Employee number must be unique across employees and applicants!')
        return super(CustomEmployee, self).write(vals)

    @staticmethod
    def _check_excel_file(file):
        if file:
            # Decode the base64 encoded data to bytes
            file_data = base64.b64decode(file)

            # Use python-magic to check the MIME type
            mime_type = magic.from_buffer(file_data, mime=True)
            if mime_type not in ['application/vnd.ms-excel',
                                 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                raise exceptions.UserError("Please upload only Excel files.")

    def send_employee_emails(self):
        for record in self:
            if record.employee_contacts:
                # Decode the file data
                file_data = base64.b64decode(record.employee_contacts)

                # Open the Excel file
                workbook = open_workbook(file_contents=file_data)
                sheet = workbook.sheet_by_index(0)

                # Iterate over the rows
                for row in range(sheet.nrows):  # assuming first row is NOT header
                    email = sheet.cell(row, 0).value  # Email in the first column
                    subject = sheet.cell(row, 1).value  # Subject in the second column
                    # Send email
                    self.env['mail.mail'].create({
                        'email_from': self.env.user.email_formatted,
                        'email_to': email,
                        'subject': subject,
                        'body_html': '<p>Welcome in GymBeam</p>',
                    }).send()
