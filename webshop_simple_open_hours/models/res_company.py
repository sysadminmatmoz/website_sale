# -*- coding: utf-8 -*-

import pytz
import logging
from datetime import datetime
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def _tz_get(self):
        # put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
        return [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]

    @api.depends('openhours_tz')
    def _compute_tz_offset(self):
        for company in self:
            company.tz_offset = datetime.now(pytz.timezone(company.openhours_tz or 'GMT')).strftime('%z')

    openhours_tz_offset = fields.Char(compute='_compute_tz_offset', string='Timezone offset', invisible=True)
    openhours_tz = fields.Selection(_tz_get, string='Timezone', default=pytz.timezone('Europe/Brussels'))
    openhours_open = fields.Float(string='Hour Opening from', help="Start time of shop availability.", store=True)
    openhours_close = fields.Float(string='Hour Opening to', help="Start time of shop availability.", store=True)

    def is_between_open_hours(self, a_daytime):
        if self.openhours_open <= float(a_daytime.hour + a_daytime.minute/60) <= self.openhours_open:
            return True
        else:
            return False

    @staticmethod
    def get_hh_mm_as_str(a_float):
        return "{:02d}:{:02d}".format(int(a_float), int(a_float % 1 * 60))
