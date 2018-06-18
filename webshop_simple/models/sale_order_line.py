# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    breadtype = fields.Many2one('category.breadtype.line', string="Bread Type")
    sizetag = fields.Many2one('category.sizetag.line', string="Size Tag")
    sides = fields.Many2many('product.product', string="Sides")
    product_price_unit = fields.Float(string='Product Price', default=0.0, compute='_compute_ppu')

    def _compute_ppu(self):
        # main product
        self.product_price_unit = self.product_id.website_price
        # sizetag if any
        if self.sizetag:
            self.product_price_unit += self.sizetag.sizetag_price
        # breadtype if any
        if self.breadtype:
            self.product_price_unit += self.breadtype.breadtype_price
        # sides if anu
        if self.sides:
            for side_product in self.sides:
                self.product_price_unit += side_product.lst_price
