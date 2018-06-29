import logging
from datetime import datetime
from pprint import pformat
from odoo import models, api, fields
from odoo.http import request
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'
    allow_week_menu_notification = fields.Boolean(default=True)

    @api.multi
    def cron_week_menu_mailing(self):
        """ Send mass mailing to all registered portal users """
        context = {}
        if self.env.context:
            context.update(self.env.context)
        context['promo'] = {}
        company = self.env.user.company_id
        if not company.week_menu_product_id:
            return
        context['promo'] = {
            'product_gift': company.week_menu_product_id.name,
        }
        self.env.context = context
        template = self.env.ref('website_sale_week_menu.email_template_week_menu')
        public_users = self.env['res.users'].search([])
        for user in public_users:
            if user.has_group('base.group_portal'):
                if user.partner_id.allow_week_menu_notification:
                    template.send_mail(user.id, force_send=True)
        return
