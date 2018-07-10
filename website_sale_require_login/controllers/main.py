# -*- coding: utf-8 -*-
# © 2018 AbAKUS IT Solutions
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class RequireLoginToAddToCart(WebsiteSale):
    @http.route(auth="user")
    def cart_update(self, **post):
        return super(RequireLoginToAddToCart, self).cart_update(**post)
