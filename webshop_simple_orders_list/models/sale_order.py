# -*- coding: utf-8 -*-
#
import pytz
import logging
from datetime import datetime, timedelta
from odoo import models, api, fields, _

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_state = fields.Selection(related='payment_tx_id.state')

    @api.multi
    def action_print_and_done(self):
        # Send the status email
        template = self.env.ref('webshop_simple_orders_list.email_template_sale_order_ready')
        template.send_mail(self.id, force_send=True)

        # Set to done
        super(SaleOrder, self).action_done()
        
        # Print the labels
        return self.action_print_labels()
