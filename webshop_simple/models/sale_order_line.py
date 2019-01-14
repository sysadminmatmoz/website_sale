# -*- coding: utf-8 -*-

import logging
from pprint import pformat
from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    breadtype = fields.Many2one('category.breadtype.line', string="Bread Type")
    sizetag = fields.Many2one('category.sizetag.line', string="Size Tag")
    sides = fields.Many2many('product.template', string="Sides")
    product_price_unit = fields.Float(string='Product Price', default=0.0, compute='_compute_ppu')
    alias = fields.Char(string="Eater Alias")

    @api.depends('breadtype', 'sizetag', 'sides', 'product_id')
    def _compute_ppu(self):
        # main product
        #self.product_price_unit = self.product_id.website_price
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

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'product_price_unit')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line. Now using product_price_unit instead of price_unit
        """
        for line in self:
            line._compute_ppu()
            price = line.product_price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price,
                                            line.order_id.currency_id,
                                            line.product_uom_qty,
                                            product=line.product_id,
                                            partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
