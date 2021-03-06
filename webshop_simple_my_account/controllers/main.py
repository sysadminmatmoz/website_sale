# -*- coding: utf-8 -*-
import logging

from pprint import pformat
from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.website_sale.controllers.main import WebsiteSale
website_account.OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name", "street", "city", "country_id"]

_logger = logging.getLogger(__name__)


class WebsiteAccountSimple(website_account):
    """ We remove zip, city and country from mendatory fields list"""
    MANDATORY_BILLING_FIELDS = ["name", "phone", "email"]

    def details_form_validate(self, data):
        """ Override this so we can add and use extra billing fields """
        return super(WebsiteAccountSimple, self).details_form_validate(data)


class WebsiteSaleSimple(WebsiteSale):

    def _get_mandatory_billing_fields(self):
        """ Remove street, city and country_id """
        return ["name", "phone", "email"]

    def _get_mandatory_shipping_fields(self):
        """ Remove street, city and country_id"""
        return ["name", "phone", "email"]
