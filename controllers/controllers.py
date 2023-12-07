# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request
import json
import logging


class ApplicantController(http.Controller):
    _logger = logging.getLogger(__name__)

    @http.route('/case_study/applicant/get', type='json', auth='public', methods=['POST'])
    def create_applicant(self):
        data = json.loads(request.httprequest.data)
        for candidate in data.get('candidates', []):
            # search for the job using api_id
            job_record = request.env['hr.job'].search([('api_id', '=', str(candidate['job']['id']))], limit=1)
            if not job_record:
                self._logger.info(f"No job found for api_id: {candidate['job']['id']}")
                continue

            # create the applicant and link to the job
            try:
                new_applicant = request.env['hr.applicant'].sudo().create({
                    'name': f"{candidate['firstname']} {candidate['surname']}",
                    'partner_phone': candidate['phone'],
                    'email_from': candidate['email'],
                    'gender': candidate['gender'],
                    'job_id': job_record.id
                })
                self._logger.info(f"New applicant created: {new_applicant.id}")
            except Exception as e:
                self._logger.error(f"Error creating applicant: {e}")

        return {'status': 'success'}
