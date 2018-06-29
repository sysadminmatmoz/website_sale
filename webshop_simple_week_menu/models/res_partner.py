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
        _logger.debug("ABAKUS: Week Menu Mailing - START")
        context = {}
        if self.env.context:
            context.update(self.env.context)
        context['promo'] = {}
        company = self.env.user.company_id
        if not company.week_menu_product_id:
            _logger.debug("ABAKUS: Week Menu Mailing - NO WEEK MENU SET - STOP")
            return
        _logger.debug("ABAKUS: Week Menu Mailing - Menu: {}".format(company.week_menu_product_id.name))
        context['promo'] = {
            'product_gift': company.week_menu_product_id.name,
        }
        self.env.context = context
        template = self.env.ref('webshop_simple_week_menu.email_template_week_menu')
        public_users = self.env['res.users'].search([])
        _logger.debug("ABAKUS: Week Menu Mailing - Users num: {}".format(len(public_users)))
        for user in public_users:
            if user.has_group('base.group_portal'):
                if user.partner_id.allow_week_menu_notification:
                    _logger.debug("ABAKUS: Week Menu Mailing - SEND TO: {}".format(user.name))
                    template.send_mail(user.id, force_send=True)
                else:
                    _logger.debug("ABAKUS: Week Menu Mailing - DISABLED FOR: {}".format(user.name))
            else:
                _logger.debug("ABAKUS: Week Menu Mailing - SKIP USER: {}".format(user.name))

        return
