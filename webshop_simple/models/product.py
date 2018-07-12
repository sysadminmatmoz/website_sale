# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    has_base_products = fields.Boolean(default=False,
                                       help="All product from this category are equivalent in nature."
                                            "They can be displayed in a single choice select widget")
