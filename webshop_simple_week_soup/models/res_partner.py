# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import logging
from pprint import pformat
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'
    # we keep this one and we should move it to webshop_simple
    # allow_week_menu_notification = fields.Boolean(default=True)

    @api.multi
    def cron_week_soup_mailing(self):
        """ Send mass mailing to all registered portal users """
        _logger.debug(u"ABAKUS: Week Soup Mailing - START")
        context = {}
        if self.env.context:
            context.update(self.env.context)
        context['promo'] = {}
        company = self.env.user.company_id
        if not company.monday_soup_id and not company.tuesday_soup_id.name \
                and not company.wednesday_soup_id.name and not company.thursday_soup_id.name\
                and not company.friday_soup_id.name:
            _logger.debug(u"ABAKUS: Week Soup Mailing - NO WEEK SOUP SET - STOP")
            return
        """ If at least one is set we proceed. This allow to handle special weeks with days off"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if company.monday_soup_id:
            context['promo']['monday'] = {
                'name': company.monday_soup_id.name,
                'url': u'{}/web/image/product.product/{}/image'.format(base_url, company.monday_soup_id.id),
            }
        if company.tuesday_soup_id:
            context['promo']['tuesday'] = {
                'name': company.tuesday_soup_id.name,
                'url': u'{}/web/image/product.product/{}/image'.format(base_url, company.tuesday_soup_id.id),
            }
        if company.wednesday_soup_id:
            context['promo']['wednesday'] = {
                'name': company.wednesday_soup_id.name,
                'url': u'{}/web/image/product.product/{}/image'.format(base_url, company.wednesday_soup_id.id),
            }
        if company.thursday_soup_id:
            context['promo']['thursday'] = {
                'name': company.thursday_soup_id.name,
                'url': u'{}/web/image/product.product/{}/image'.format(base_url, company.thursday_soup_id.id),
            }
        if company.friday_soup_id:
            context['promo']['friday'] = {
                'name': company.friday_soup_id.name,
                'url': u'{}/web/image/product.product/{}/image'.format(base_url, company.friday_soup_id.id),
            }

        self.env.context = context
        template = self.env.ref('webshop_simple_week_soup.email_template_week_soup')
        public_users = self.env['res.users'].search([])
        _logger.debug(u"ABAKUS: Week Soup Mailing - Users num: {}".format(len(public_users)))
        for user in public_users:
            if user.has_group('base.group_portal'):
                if user.partner_id.allow_week_menu_notification:
                    _logger.debug(u"ABAKUS: Week Soup Mailing - SEND TO: {}".format(user.name))
                    template.send_mail(user.id, force_send=True)
                else:
                    _logger.debug(u"ABAKUS: Week Soup Mailing - DISABLED FOR: {}".format(user.name))
            else:
                _logger.debug(u"ABAKUS: Week Soup Mailing - SKIP USER: {}".format(user.name))

        return
