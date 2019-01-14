# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import pytz
import datetime
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    monday_product_id = fields.Many2one('product.product', string='Monday Product')
    tuesday_product_id = fields.Many2one('product.product', string='Tuesday Product')
    wednesday_product_id = fields.Many2one('product.product', string='Wednesday Product')
    thursday_product_id = fields.Many2one('product.product', string='Thursday Product')
    friday_product_id = fields.Many2one('product.product', string='Friday Product')

    def get_named_day_product(self):
        """ A day takes into account open/closing day so
          tuesday is actually from monday open hour to tuesday closing hour """
        now = datetime.datetime.now(pytz.timezone(self.openhours_tz))
        # week_day = datetime.datetime.now(pytz.timezone('Europe/Brussels')).weekday()
        week_day = now.weekday()
        position = self.is_between_open_hours(now)
        if week_day == 0:
            if position == 1:
                return self.tuesday_product_id
            else:
                return self.monday_product_id
        elif week_day == 1:
            if position == 1:
                return self.wednesday_product_id
            else:
                return self.tuesday_product_id
        elif week_day == 2:
            if position == 1:
                return self.thursday_product_id
            else:
                return self.wednesday_product_id
        elif week_day == 3:
            if position == 1:
                return self.friday_product_id
            else:
                return self.thursday_product_id
        elif week_day == 4:
            if position == 1:
                return self.monday_product_id
            else:
                return self.friday_product_id
        else:
            return self.monday_product_id
