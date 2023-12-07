from odoo import models, fields
import random


class CustomJobPosition(models.Model):
    _inherit = 'hr.job'

    def _generate_unique_api_id(self):
        while True:
            api_id = str(random.randint(10000000, 99999999))  # generate a 8-digit number string
            if not self.with_context(active_test=False).search_count([('api_id', '=', api_id)]):
                return api_id

    api_id = fields.Char(string='API ID', default=_generate_unique_api_id, readonly=True, required=True)
