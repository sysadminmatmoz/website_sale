# -*- coding: utf-8 -*-
#
import logging
from odoo import models, api, fields, _

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = 'product.category'

    wait_message = fields.Text(translate=True)