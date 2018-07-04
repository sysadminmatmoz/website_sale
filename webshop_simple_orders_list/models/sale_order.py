# -*- coding: utf-8 -*-
#
import pytz
import logging
from datetime import datetime, timedelta
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_state = fields.Selection(related='payment_tx_id.state')

    def filter_today_action(self):
        # check company_id
        company_id = self.env.user.company_id
        # NOTE: use timezone when fetching today
        today = datetime.now(pytz.timezone(company_id.openhours_tz or 'GMT'))
        yesterday = today - timedelta(days=1)
        from_date = "{} {:02d}:{:02d}:00".format(
            yesterday.strftime('%Y-%m-%d'),
            int(company_id.openhours_open),
            int(company_id.openhours_open % 1 * 60))
        to_date = "{} {:02d}:{:02d}:00".format(
            today.strftime('%Y-%m-%d'),
            int(company_id.openhours_close),
            int(company_id.openhours_close % 1 * 60))
        tree_id = self.env.ref("webshop_simple_orders_list.view_simple_orders_tree")
        form_id = self.env.ref("webshop_simple_orders_list.view_simple_orders_form")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Today\'s Orders',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [
                ('state', 'in', ['sale', 'done']),
                ('payment_state', '=', 'done'),
                ('confirmation_date', '>=', from_date),
                ('confirmation_date', '<=', to_date)],
            # if you don't want to specify form for example
            # (False, 'form') just pass False
            'views': [(tree_id.id, 'tree'), (form_id.id, 'form')],
            'target': 'current',
            'context': None,
        }

    def filter_tomorrow_action(self):
        # check company_id
        company_id = self.env.user.company_id
        # NOTE: use timezone when fetching today
        today = datetime.now(pytz.timezone(company_id.openhours_tz or 'GMT'))
        from_date = "{} {:02d}:{:02d}:00".format(
            today.strftime('%Y-%m-%d'),
            int(company_id.openhours_open),
            int(company_id.openhours_open % 1 * 60))
        tree_id = self.env.ref("webshop_simple_orders_list.view_simple_orders_tree")
        form_id = self.env.ref("webshop_simple_orders_list.view_simple_orders_form")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tomorrow\'s Orders',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [
                ('state', 'in', ['sale', 'done']),
                ('payment_state', '=', 'done'),
                ('confirmation_date', '>=', from_date)],
            # if you don't want to specify form for example
            # (False, 'form') just pass False
            'views': [(tree_id.id, 'tree'), (form_id.id, 'form')],
            'target': 'current',
            'context': None,
        }

    @api.multi
    def action_done(self):
        """ Send a confirmation email before setting to done """
        context = {
            'order': {
                'name': self.name,
                'description': self.display_name,
            }
        }
        self.env.context = context
        template = self.env.ref('webshop_simple_orders_list.email_order_is_ready')
        template.send_mail(self.partner_id.id, force_send=True)
        return super(SaleOrder, self).action_done()
