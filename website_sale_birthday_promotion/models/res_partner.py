# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from pprint import pformat
from odoo import models, api, fields
from odoo.http import request
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bday = fields.Integer('Birthday Day')
    bmonth = fields.Integer('Birthday Month')
    is_bday_gift_available = fields.Boolean('is Birthday Gif Available', default=False)

    @api.multi
    def cron_birthday_promotion_mailing(self):
        """ Send mass mailing to all registered portal user with the right flag on """
        context = {}
        if self.env.context:
            context.update(self.env.context)
        context['promo'] = {}
        company = self.env.user.company_id
        if not company.birthday_promotion_product_id:
            return
        context['promo'] = {
            'product_gift': company.birthday_promotion_product_id.name,
        }
        self.env.context = context
        template = self.env.ref('website_sale_birthday_promotion.email_template_user_birthday')
        today = datetime.now()
        public_users = self.env['res.users'].search([])
        for user in public_users:
            if user.has_group('base.group_portal'):
                if user.partner_id.bday == int(today.strftime('%d')) and user.partner_id.bmonth == int(today.strftime('%m')):
                    template.send_mail(user.id, force_send=True)
                    user.write({'is_bday_gift_available': True})
                elif user.partner_id.is_bday_gift_available:
                    # unset flag when promotion unused
                    user.write({'is_bday_gift_available': False})
        return
