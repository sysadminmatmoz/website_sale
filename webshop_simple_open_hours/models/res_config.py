# -*- coding: utf-8 -*-

import logging
import math

from datetime import date, time
from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)


class WebsiteConfigSettings(models.TransientModel):
    """ Promotion main class """
    _inherit = 'website.config.settings'

    openhours_open = fields.Float(string='Hour Opening from', help="Start time of shop availability.", store=True)
    openhours_close = fields.Float(string='Hour Opening to', help="Start time of shop availability.", store=True)

    def is_between_open_hours(self, a_daytime):
        if self.get_hour(self.openhours_close) >=  a_daytime.hour >= self.get_hour(self.openhours_open):
            return True
        else:
            return False

    @staticmethod
    def round_the_mnumbers(value):
        x = math.floor(value)
        if (value - x) < .50:
            return x
        else:
            return math.ceil(value)

    def get_min(self, a_float):
        self.round_the_mnumbers((a_float % 1) * 60)

    def get_hour(self, a_float):
        self.round_the_mnumbers(a_float % 1)
