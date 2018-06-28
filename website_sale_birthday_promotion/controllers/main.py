# -*- coding: utf-8 -*-
import logging

from pprint import pformat
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website_portal.controllers.main import website_account

_logger = logging.getLogger(__name__)


class WebsiteAccount(website_account):

    OPTIONAL_BILLING_FIELDS = website_account.OPTIONAL_BILLING_FIELDS + ["bday", "bmonth"]

    def details_form_validate(self, data):
        return super(WebsiteAccount, self).details_form_validate(data)
