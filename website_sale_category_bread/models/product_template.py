# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, tools, _
from pprint import pformat
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    """
    Add breadtype property to product
    """
    _inherit = 'product.template'

    has_breadtype = fields.Boolean(related='categ_id.has_breadtype')
    breadtype_line_ids = fields.One2many('category.breadtype.line', 'product_id', string="Size Tag Lines", copy=True)
