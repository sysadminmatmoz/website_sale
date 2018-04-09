# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, exceptions, _
from pprint import pformat
_logger = logging.getLogger(__name__)


class PublicCategory(models.Model):
    _inherit = 'product.public.category'

    products_count = fields.Integer(compute='_compute_products_count')

    @api.one
    def _compute_products_count(self):
        count = len(self.env['product.template'].search([('public_categ_ids.id', '=', self.id)]))
        for child in self.child_id:
            count = count + child.products_count
        self.products_count = count