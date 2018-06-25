# -*- coding: utf-8 -*-
#
import logging
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_state = fields.Selection(related='payment_tx_id.state')
