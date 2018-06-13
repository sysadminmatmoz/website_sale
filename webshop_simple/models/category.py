# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, tools, _
_logger = logging.getLogger(__name__)


class Category(models.Model):
    _inherit = 'product.public.category'
