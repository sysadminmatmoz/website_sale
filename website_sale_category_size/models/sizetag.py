# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, tools, _
_logger = logging.getLogger(__name__)


class SizeTag(models.Model):
    """
    We add a size manager that can be used by all products from a category has it enabled.
    """
    _name = 'category.sizetag'
    _description = 'Category Size tag'

    name = fields.Char()
    active = fields.Boolean(default=True)


class SizeTageLine(models.Model):
    """
    Allows coupling a Size Tag with a price
    """
    _name = 'category.sizetag.line'
    _description = 'Category Size tag Line'

    product_id = fields.Many2one('product.template', string="Product")
    sizetag_id = fields.Many2one('category.sizetag', string="Size Tag", ondelete='cascade', required=True)
    sizetag_price = fields.Float(string='Size Tag Price', default=0.0)

    @api.multi
    def name_get(self):
        result = []
        for line in self:
            if line.sizetag_price > 0:
                result.append((line.id, line.sizetag_id.name + " (+ " + str(line.sizetag_price) + ")"))
            else:
                result.append((line.id, line.sizetag_id.name))
        return result