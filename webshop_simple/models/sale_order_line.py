# -*- coding: utf-8 -*-

import logging
from pprint import pformat
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sides = fields.Many2many('product.product', string="Sides")
    product_price_unit = fields.Float(string='Product Price', default=0.0)

    @api.model
    def create(self, vals):
        # product_id gives the initial price
        if 'product_id' not in vals:
            raise ValidationError('Missing product_id')
        main_product = self.env['product.template'].search([('id', '=', vals['product_id'])])
        # Check with VT: why is website_price used here ??
        ppu = main_product.website_price
        if main_product.has_sizetag and 'sizetag' in vals:
            for stl in main_product.sizetags_line_ids:
                if stl.sizetag_id == vals.get('sizetags'):
                    ppu += stl.sizetag_price
        if main_product.has_breadtype and 'breadtype' in vals:
            for btl in main_product.breatype_line_ids:
                if btl.sizetag_id == vals.get('breadtype'):
                    ppu += btl.breadtype_price
        if 'sides' in vals:
            for side_id in vals['sides']:
                side_product = self.env['product.template'].search([('id', '=', int(side_id))])
                # Check with VT : and here we take the lst_price
                ppu += side_product.lst_price
        # update vals
        vals['product_price_unit'] = ppu
        _logger.debug('ABAKUS: vals={}'.format(pformat(vals, depth=4)))

        return super(SaleOrderLine, self).create(vals)

