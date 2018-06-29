# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, tools, _
_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    """
    This image will be used as header of the sale order label report
    """
    _inherit = 'res.company'

    label_report_logo = fields.Binary(string="Label Report Logo")
