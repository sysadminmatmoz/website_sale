# -*- coding: utf-8 -*-
import logging
from odoo.http import request
from odoo.addons.webshop_simple.controllers.main import WebsiteSaleSimple
from odoo.addons.website_portal.controllers.main import website_account
website_account.OPTIONAL_BILLING_FIELDS += ['product_promotion_notification']

_logger = logging.getLogger(__name__)


class WebsiteAccountPromoNotification(website_account):

    OPTIONAL_BILLING_FIELDS = website_account.OPTIONAL_BILLING_FIELDS

    def details_form_validate(self, data):
        """ Override this so we can add and use extra billing fields """
        if 'product_promotion_notification' in data:
            data['product_promotion_notification'] = True
        else:
            data['product_promotion_notification'] = False
        return super(WebsiteAccountPromoNotification, self).details_form_validate(data)


class WebsiteSimplePromos(WebsiteSaleSimple):

    @staticmethod
    def shop_simple_category_render(page, values):
        # Get all promo product from this week
        promo_record = request.env['product.promotion'].sudo().search([('state', '=', 'curr')], limit=1)
        _logger.debug("ABAKUS: found ({}) promo records".format(len(promo_record)))
        if promo_record:
            promo_record = promo_record[0]
            _logger.debug("ABAKUS: categ:{} - sand cat:{} - sal cat:{}".format(
                values['category'].id, promo_record.product_sandwich.categ_id.id, promo_record.product_salad.categ_id.id))
            if 'category' in values:
                if values['category'].id == promo_record.product_sandwich.categ_id.id:
                    values['promo_product_id'] = promo_record.product_sandwich
                    values['promo_product_price'] = promo_record.product_sandwich_promo_price
                elif values['category'].id == promo_record.product_salad.categ_id.id:
                    values['promo_product_id'] = promo_record.product_salad
                    values['promo_product_price'] = promo_record.product_salad_promo_price
            _logger.debug("ABAKUS: values products - {}".format(values))
        return request.render(page, values)
