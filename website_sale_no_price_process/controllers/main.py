# -*- coding: utf-8 -*-
import json
import logging
from werkzeug.exceptions import Forbidden

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.base.ir.ir_qweb.fields import nl2br
from odoo.addons.website.controllers.main import QueryURL
from odoo.exceptions import ValidationError
from odoo.addons.website_form.controllers.main import WebsiteForm

_logger = logging.getLogger(__name__)

class WebsiteSale(http.Controller):

    @http.route('/shop/quotation/validate', type='http', auth="public", website=True)
    def quotation_validate(self, **post):
        order = request.website.sale_get_order()
        order.partner_id.write({'last_website_so_id': False})
        request.website.sale_reset()

        return request.redirect('/shop/')
