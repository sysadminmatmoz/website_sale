# -*- coding: utf-8 -*-
import logging

from odoo.addons.website_portal.controllers.main import website_account
website_account.OPTIONAL_BILLING_FIELDS += ['product_promotion_notification']

_logger = logging.getLogger(__name__)


class WebsiteAccountPromoNotification(website_account):

    OPTIONAL_BILLING_FIELDS = website_account.OPTIONAL_BILLING_FIELDS

    def details_form_validate(self, data):
        """ Override this so we can add and use extra billing fields """
        return super(WebsiteAccountPromoNotification, self).details_form_validate(data)
