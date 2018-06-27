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

    @api.multi
    def cron_promotion_mailing(self):
        """ Send mass mailing to all registered portal user with the right flag on """
        context = {}
        if self.env.context:
            context.update(self.env.context)
        context['promo'] = {}
        company = self.env.res_user.company
        if not company.birthday_promotion_product_id:
            return
        context['promo'] = {
            'product_gift': company.birthday_promotion_product_id.name,
        }
        self.env.context = context
        template = self.env.ref('website_sale_birthday_promotion.email_template_user_birthday')
        today = datetime.datetime.now()
        public_users = self.env['res.users'].search([
            ('partner_id.bday', '=', int(today.strftime('%d'))),
            ('partner_id.bmonth', '=', int(today.strftime('%m')))
        ])
        for user in public_users:
            if user.has_group('base.public_user'):
                _logger.debug("ABAKUS: Birthday omotion email sent")
                template.send_mail(user.id, force_send=True)
        return
