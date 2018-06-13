# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, tools, _
_logger = logging.getLogger(__name__)


class BreadType(models.Model):
    """
    We add a size manager that can be used by all products from a category has it enabled.
    """
    _name = 'category.breadtype'
    _description = 'Category Bread Type'

    name = fields.Char()
    active = fields.Boolean(default=False)


class BreadTypeLine(models.Model):
    """
    Allows coupling a Bread Type with a price
    """
    _name = 'category.breadtype.line'
    _description = 'Category Bread Type Line'

    product_id = fields.Many2one('product.template', string="Product")
    breadtype_id = fields.Many2one('category.breadtype', string="Bread Type", ondelete='cascade', required=True)
    breadtype_price = fields.Float(string='Bread Type Price', default=0.0)
