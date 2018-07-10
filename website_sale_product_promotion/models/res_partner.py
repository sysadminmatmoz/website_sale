# -*- coding: utf-8 -*-
import pytz
import logging
from datetime import datetime
from pprint import pformat
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_promotion_notification = fields.Boolean(default=True)
