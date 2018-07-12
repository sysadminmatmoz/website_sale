# -*- coding: utf-8 -*-
#
import pytz
import logging
from datetime import datetime, timedelta
from odoo import models, api, fields, _

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_print_labels(self):
        return self.env['report'].get_action(self, 'website_sale_order_label.website_sale_label_report')
