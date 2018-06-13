# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, tools, _
_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    """
    This flag controls the availability of breadtypes in all product from the category
    """
    _inherit = 'product.category'

    has_breadtype = fields.Boolean(default=False)
