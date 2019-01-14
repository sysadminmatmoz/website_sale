# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import pytz
import datetime
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    monday_soup_id = fields.Many2one('product.product', string='Monday Soup')
    tuesday_soup_id = fields.Many2one('product.product', string='Tuesday Soup')
    wednesday_soup_id = fields.Many2one('product.product', string='Wednesday Soup')
    thursday_soup_id = fields.Many2one('product.product', string='Thursday Soup')
    friday_soup_id = fields.Many2one('product.product', string='Friday Soup')

    def get_named_day_soup(self):
        """ A day takes into account open/closing day so
          tuesday is actually from monday open hour to tuesday closing hour """
        now = datetime.datetime.now(pytz.timezone(self.openhours_tz))
        week_day = now.weekday()
        position = self.is_between_open_hours(now)
        if week_day == 0:
            if position == 1:
                return self.tuesday_soup_id
            else:
                return self.monday_soup_id
        elif week_day == 1:
            if position == 1:
                return self.wednesday_soup_id
            else:
                return self.tuesday_soup_id
        elif week_day == 2:
            if position == 1:
                return self.thursday_soup_id
            else:
                return self.wednesday_soup_id
        elif week_day == 3:
            if position == 1:
                return self.friday_soup_id
            else:
                return self.thursday_soup_id
        elif week_day == 4:
            if position == 1:
                return self.monday_soup_id
            else:
                return self.friday_soup_id
        else:
            return self.monday_soup_id
