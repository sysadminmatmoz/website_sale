# -*- coding: utf-8 -*-

import pytz
import logging
from datetime import datetime, timedelta

from odoo import http, tools, _
from odoo.http import request
import odoo.addons.webshop_simple.controllers.main as main

_logger = logging.getLogger(__name__)


class WebsiteSaleDerived(main.WebsiteSale):
    """ Override method in order to check open hours first """
    # @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    @http.route(['/shop/cart/update'], type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        company = request.env.user.company_id
        now = datetime.now(pytz.timezone(company.openhours_tz))
        # check if we are within open hours
        position = company.is_between_open_hours(now)
        if position == 2:
            kw['delivery_date'] = now + timedelta(days=1)
            # redirect to original cart update
            return super(WebsiteSaleDerived, self).cart_update(product_id, add_qty=add_qty, set_qty=set_qty, **kw)
        elif position == 1:
            kw['delivery_date'] = now
            # redirect to original cart update
            return super(WebsiteSaleDerived, self).cart_update(product_id, add_qty=add_qty, set_qty=set_qty, **kw)
        else:
            # position==0, we are closed, redirect to message page
            values = {
                'openhours_open': company.get_hh_mm_as_str(company.openhours_open),
                'openhours_close': company.get_hh_mm_as_str(company.openhours_close),
                'now': now,
            }
        return request.render("webshop_simple_open_hours.open_hours", values)

