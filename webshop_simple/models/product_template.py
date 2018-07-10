# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, tools, _
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    """
    a Base side product will appear in single select drop down menu in category view
    """
    _inherit = 'product.template'

    is_base_side = fields.Boolean(default=False)
