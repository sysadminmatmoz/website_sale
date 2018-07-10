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
    def action_done(self):
        """ Send a confirmation email before setting to done """
        mail_mail = self.env['mail.mail']
        mail_txt = _("Your order ({}) is ready !".format(self.name))
        mail_id = mail_mail.create({
            'body_html': mail_txt,
            'subject': 'Order Ready Notification',
            'email_to': self.partner_id.email,
            'email_from': self.company_id.email,
            'state': 'outgoing',
            'auto_delete': True,
        })
        mail_mail.send([mail_id])
        return super(SaleOrder, self).action_done()
