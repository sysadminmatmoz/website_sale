# -*- coding: utf-8 -*-
#
import pytz
import logging
from pprint import pformat
from datetime import datetime, timedelta
from odoo import models, api, fields, _
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            company = self.env['res.company'].browse(vals['company_id'])
            now = datetime.now(pytz.timezone(company.openhours_tz))
            position = company.is_between_open_hours(now)
            vals['delivery_date'] = now.strftime("%Y-%m-%d")
            if position == 1:
                vals['delivery_date'] = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        return super(SaleOrder, self).create(vals)



