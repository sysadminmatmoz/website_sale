# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, tools, _
_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    """
    We add a size manager that can be used by all products from a category has it enabled.
    """
    _inherit = 'product.category'

    has_sizetag = fields.Boolean(default=False)
