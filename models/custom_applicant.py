# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
import random


class CustomApplicant(models.Model):
    _inherit = 'hr.applicant'
    # a unique employee tracking number
    employee_number = fields.Char(string='Employee Number', required=True, tracking=True)
    gender = fields.Char(string='Gender')

    @api.model
    def create(self, vals):
        # ensures uniqueness of `employee_number` across system
        if 'employee_number' not in vals or not vals['employee_number']:
            # give a unique random 8-digit number if not given (this is necessary to make the online job posts work)
            vals['employee_number'] = self._generate_unique_employee_number()
        else:
            # Check against employees (active and archived)
            employee_count = self.env['hr.employee'].with_context(active_test=False).search_count(
                [('employee_number', '=', vals['employee_number'])])

            # Check against applicants (active and archived)
            applicant_count = self.env['hr.applicant'].with_context(active_test=False).search_count(
                [('employee_number', '=', vals['employee_number'])])

            if employee_count or applicant_count:
                raise exceptions.ValidationError('Employee number must be unique across employees and applicants!')

        return super(CustomApplicant, self).create(vals)

    def write(self, vals):
        # ensures uniqueness of `employee_number` across system
        if 'employee_number' in vals:
            for record in self:
                # Check against employees (active and archived)
                employee_count = self.env['hr.employee'].with_context(active_test=False).search_count(
                    [('employee_number', '=', vals['employee_number'])])

                # Check against other applicants (active and archived)
                applicant_count = self.env['hr.applicant'].with_context(active_test=False).search_count(
                    [('employee_number', '=', vals['employee_number']), ('id', '!=', record.id)])

                if employee_count or applicant_count:
                    raise exceptions.ValidationError('Employee number must be unique across employees and applicants!')
        return super(CustomApplicant, self).write(vals)

    def _generate_unique_employee_number(self):
        # If the number is not unique, loop again to generate a new number
        while True:
            # Generate a random 8-digit number
            random_number = str(random.randint(10000000, 99999999))

            # Check if this number is unique across employees and applicants
            if not (self.env['hr.employee'].with_context(active_test=False).search_count(
                    [('employee_number', '=', random_number)]) or
                    self.env['hr.applicant'].with_context(active_test=False).search_count(
                        [('employee_number', '=', random_number)])):
                return random_number
