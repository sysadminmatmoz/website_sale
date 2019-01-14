# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def _is_public(self):
        """ borrowed from Odoo 11"""
        self.ensure_one()
        return self.has_group('base.group_public')

    @api.multi
    def _is_portal(self):
        """ adapted from the one above """
        self.ensure_one()
        return self.has_group('base.group_portal')

    @api.multi
    def _has_birthday_gift(self):
        self.ensure_one()
        if self.partner_id:
            return self.partner_id.is_bday_gift_available
        else:
            return False

    @api.model
    def create(self, values):
        """
        Default phone number to avoid displaying shop/address
        Default country_id to allow payment
        """
        if not values.get('phone'):
            values['phone'] = u'+32477353535'
        user = super(ResUsers, self).create(values)
        company_id = self.env['res.company']._company_default_get('webshop.simple')
        if company_id and company_id.country_id:
            user.partner_id.write({'country_id': company_id.country_id.id})
        else:
            _logger.warning("ABK: No country set for company [{}]".format(company_id.name))
        return user
