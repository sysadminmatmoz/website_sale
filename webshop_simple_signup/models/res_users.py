# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from pprint import pformat
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResUsersExtraFields(models.Model):
    _inherit = 'res.users'

    @api.model
    def signup(self, values, token=None):
        # First create user with partner entry
        _logger.debug("ABAKUS: RES USER BEF values={}".format(pformat(values, depth=4)))
        db, login, password = super(ResUsersExtraFields, self).signup(values, token)
        # now add etra fields to partner
        self.partner.write({
            'birth_day': values.get('birth_day'),
            'birth_month': values.get('birth_month'),
            'phone': values.get('phone'),
        })
        _logger.debug("ABAKUS: RES USER AFT values={}".format(pformat(values, depth=4)))
        return db, login, password
