# -*- coding: utf-8 -*-
import logging
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    birth_day = fields.Integer('Birth Day')
    birth_month = fields.Integer('Birth Month')
