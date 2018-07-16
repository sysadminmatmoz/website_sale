# -*- coding: utf-8 -*-

import logging
from pprint import pformat
from datetime import date
from datetime import timedelta
from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)


class ProductPromotion(models.Model):
    """ Promotion main class """
    _name = 'product.promotion'

    name = fields.Char(index=True, readonly=True, required=True, default=lambda self: _('New'))
    sequence = fields.Integer('Sequence', default=1, help='Gives the sequence order when displaying promotions')
    description = fields.Text(translate=True, help="A description of the promotion")
    display_name = fields.Char(string='Name', compute='_compute_display_name')
    date_beg = fields.Datetime(default=date.today())
    date_end = fields.Datetime(computed="_compute_date_end", readonly=True, default=date.today() + timedelta(weeks=1))
    product_first = fields.Many2one('product.product', 'First product')
    product_second = fields.Many2one('product.product', 'Second product')
    state = fields.Selection([
        ('draft', _('Draft')),
        ('next', _('Next')),
        ('curr', _('Current')),
        ('closed', _('Closed'))], string='Status', default='draft', required=True)

    _sql_constraints = [
        ('name', 'UNIQUE (name)', 'Your already have a promotion for this week.'),
    ]

    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = fields.Datetime.from_string(values['date_beg']).strftime('%Yw%V')
        return super(ProductPromotion, self).create(values)

    @api.one
    @api.depends('date_beg')
    def _compute_display_name(self):
        # %Y - year as YYYY
        # %W - week number of the current year, starting with the first Monday as the first day of the first week.
        self.display_name = "{} - [{} - {}]".format(
            fields.Datetime.from_string(self.date_beg).strftime('%Yw%V'),
            fields.Datetime.from_string(self.date_beg).strftime('%Y-%m-%d'),
            fields.Datetime.from_string(self.date_end).strftime('%Y-%m-%d'))

    @api.onchange('date_beg')
    def _compute_date_end(self):
        self.date_end = (fields.Date.from_string(self.date_beg) + timedelta(weeks=1)).strftime('%Y-%m-%d')

    @api.multi
    def cron_promotion_creation_check(self):
        """ Check if we have a scheduled promotion for next week. If not notify managers.
        NOTE: promo is set to current manually by the admin """
        # monday = weekday #0
        days_ahead = 7 - date.today().weekday()
        next_monday = date.today() + timedelta(days_ahead)
        next_week_name = next_monday.strftime('%Yw%V')
        promo_count = self.env['product.promotion'].search_count([
            ('state', '=', 'next'),
            ('name', '=', next_week_name)])
        res = 'PASSED'
        if promo_count == 0:
            res = 'FAILED'
            user_manager_ids = self.env['res.users'].search([])
            for manager in user_manager_ids:
                if manager.has_group('sales_team.group_sale_manager'):
                    mail_mail = self.env['mail.mail']
                    mail_txt = _("Please remember to create a promotion for week {}".format(next_week_name))
                    mail_id = mail_mail.create({
                                    'body_html': mail_txt,
                                    'subject': 'Odoo Promotion Creation Notification',
                                    'email_to': manager.partner_id.mail,
                                    'email_from': self.env.user.company_id.email,
                                    'state': 'outgoing',
                                    'auto_delete': True,
                                })
                    mail_mail.send([mail_id])

        _logger.debug('Promotion Creation Check: week {} - {}'.format(next_week_name, res))

    @api.multi
    def cron_promotion_mailing(self):
        """ Send mass mailing to all registered portal user with the right flag on """
        # prepare promo data
        context = {}
        if self.env.context:
            context.update(self.env.context)
        promo_record = self.search([('state', '=', 'curr')], limit=1)
        context['promo'] = {}
        if promo_record:
            context['promo'] = {
                'description': promo_record.description,
                'product_first': promo_record.product_first.name,
                'product_second': promo_record.product_second.name,
            }
        else:
            # No promo set as current notify the admin
            user_manager_ids = self.env['res.users'].search([])
            mail_mail = self.env['mail.mail']
            mail_txt = _("Please remember to set this week's promotion to CURRENT")
            for user in user_manager_ids:
                if user.has_group('sales_team.group_sale_manager'):
                    mail_id = mail_mail.create({
                                'body_html': mail_txt,
                                'subject': 'Odoo Promotion Activation Notification',
                                'email_to': user.partner_id.email,
                                'email_from': self.env.user.company_id.email,
                                'state': 'outgoing',
                                'auto_delete': True,
                            })
                    mail_mail.send([mail_id])
            return

        self.env.context = context
        # fetch email template
        template = self.env.ref('website_sale_product_promotion.email_template_product_promotion')
        # get all public user that want a promotion notification
        public_users = self.env['res.users'].search([])
        for user in public_users:
            if user.has_group('base.group_portal'):
                # self.env['mail.template'].browse(template.id).send_mail(user.id)
                template.send_mail(user.id, force_send=True)
        return

    @api.multi
    def action_draft_to_next(self):
        return self.write({'state': 'next'})

    @api.multi
    def action_next_to_current(self):
        return self.write({'state': 'curr'})

    @api.multi
    def action_to_closed(self):
        return self.write({'state': 'closed'})

    @api.multi
    def action_back_to_draft(self):
        return self.write({'state': 'draft'})
