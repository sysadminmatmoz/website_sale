# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    birthday_promotion_product_id = fields.Many2one('product.product', string='Birthday Gift Product')
