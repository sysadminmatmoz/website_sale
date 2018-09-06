# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    monday_product_id = fields.Many2one('product.product', string='Monday Product')
    tuesday_product_id = fields.Many2one('product.product', string='Tuesday Product')
    wednesday_product_id = fields.Many2one('product.product', string='Wednesday Product')
    thursday_product_id = fields.Many2one('product.product', string='Thursday Product')
    friday_product_id = fields.Many2one('product.product', string='Friday Product')
