# -*- coding: utf-8 -*-

import logging
from pprint import pformat
from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('breadtype', 'sizetag', 'sides', 'product_id')
    def _compute_ppu(self):
        """  We over ride the coputation in webshop simple just in case we have promotion on the product """
        # base product
        promo_record = self.env['product.promotion'].sudo().search([('state', '=', 'curr')], limit=1)
        if promo_record:
            promo_record = promo_record[0]
            if promo_record.product_sandwich.id == self.product_id.id:
                self.product_price_unit = promo_record.product_sandwich_promo_price
            elif promo_record.product_salad.id == self.product_id.id:
                self.product_price_unit = promo_record.product_salad_promo_price
            else:
                self.product_price_unit = self.price_unit
        else:
            self.product_price_unit = self.price_unit
        # sizetag if any
        if self.sizetag:
            self.product_price_unit += self.sizetag.sizetag_price
        # breadtype if any
        if self.breadtype:
            self.product_price_unit += self.breadtype.breadtype_price
        # sides if any
        if self.sides:
            for side_product in self.sides:
                if side_product.has_sizetag:
                    for sizetag in side_product.sizetags_line_ids:
                        if sizetag.sizetag_id == self.sizetag.sizetag_id:
                            self.product_price_unit += sizetag.sizetag_price
                else:
                    self.product_price_unit += side_product.lst_price
