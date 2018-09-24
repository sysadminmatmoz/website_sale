# -*- coding: utf-8 -*-
import pytz
import logging
from datetime import datetime
from pprint import pformat
from odoo import models, api, fields
from odoo.addons.website.models.website import slug

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_bday_gift_available = fields.Boolean('is Birthday Gif Available', default=False)

    @api.multi
    def cron_birthday_promotion_mailing(self):
        """ Send mass mailing to all registered portal user with the right flag on """
        context = {}
        if self.env.context:
            context.update(self.env.context)
        context['promo'] = {}
        company = self.env.user.company_id
        # check if we actually have a product in promotion
        if not company.birthday_promotion_product_id:
            return
        product_id = company.birthday_promotion_product_id
        # construct product url
        # <website_domain>/shop/simple/category/<category-slug>#product_id_<id>
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # NOTE: only the first public category is used in creating the slug
        product_url = u"{}/shop/simple/category/{}#base_price_{}".format(
            base_url,
            slug(product_id.categ_id),
            product_id.id
        )
        _logger.debug("ABAKUS: url=%s" % product_url)
        context['promo'] = {
            'product_gift': product_id.name,
            'product_url': product_url,
        }
        self.env.context = context
        template = self.env.ref('website_sale_birthday_promotion.email_template_user_birthday')
        # TODO: get timezone from company
        today = datetime.now(pytz.timezone('Europe/Brussels'))
        public_users = self.env['res.users'].search([])
        for user in public_users:
            if user.has_group('base.group_portal'):
                if user.partner_id.birth_day == int(today.strftime('%d')) and user.partner_id.birth_month == int(today.strftime('%m')):
                    template.send_mail(user.id, force_send=True)
                    user.write({'is_bday_gift_available': True})
                elif user.partner_id.is_bday_gift_available:
                    # unset flag when promotion unused
                    user.write({'is_bday_gift_available': False})
        return
