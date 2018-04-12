# -*- coding: utf-8 -*-
import json
import logging
from werkzeug.exceptions import Forbidden

from odoo import http, tools, _
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.website_sale.controllers.main import WebsiteSale
_logger = logging.getLogger(__name__)

class WebsiteSaleRestricted(WebsiteSale):

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        public_user = http.request.env['res.users'].sudo().search([('login', '=', 'public'),('active', '=', False)]) # Public user default ID
        if request.uid != public_user.id:
            #only render the template with other operations
            return super(WebsiteSaleRestricted, self).shop(page, category, search, ppg)
        else:
            return request.render("website_sale_restricted_to_users.website_sale_restricted_access", {})
