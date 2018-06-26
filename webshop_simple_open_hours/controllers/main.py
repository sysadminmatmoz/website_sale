# -*- coding: utf-8 -*-

import logging
from pprint import pformat

from datetime import datetime, time

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.webshop_simple.controllers.main import WebsiteSale as WS

_logger = logging.getLogger(__name__)


class WebsiteSaleDerived(WS):
    """ Overide method in order to check open hours first """
    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        _logger.debug("ABAKUS: checking Open Hours")
        now = datetime.now()
        config = request.env['website.config.settings'].sudo().create({})
        # check if we are within open hours
        if config.is_between_open_hours(now):
            # redirect to original cart update
            _logger.debug("ABAKUS: yes, within the interval proceed to cart_update")
            return WS.cart_update(product_id, add_qty, set_qty, kw)
        else:
            # redirect to closure message page
            values = {
                'now': now,
            }
        return request.render("webshop_simple_open_hours.open_hours", values)

