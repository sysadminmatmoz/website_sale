# -*- coding: utf-8 -*-
import logging

from pprint import pformat
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteAccount(website_account):

    OPTIONAL_BILLING_FIELDS = website_account.OPTIONAL_BILLING_FIELDS + ["bday", "bmonth"]

    def details_form_validate(self, data):
        """ Override this so we can add and use extra billing fields """
        return super(WebsiteAccount, self).details_form_validate(data)


class WebisteSaleBirthdayGift(WebsiteSale):

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        """ Overide this in order to add a free birthday gift if:
        - user is logged in and it's his birthday
         """
        partner_id = int(post.get('partner_id', -1))
        if partner_id > 0 and partner_id.is_bday_gift_available:
            # Add gift product
            company = request.env.user.company_id
            product_id = company.birthday_promotion_product_id
            request.website.sale_get_order()._cart_update(
                product_id=int(product_id),
                add_qty=1,
                set_qty=1,
                attributes=None,
                is_bday_gift=True,
            )
            # reset availability so he won't get it twice.
            partner_id.sudo().write({'is_bday_gift_available': False})

        return super(WebisteSaleBirthdayGift, self).payment(post)
