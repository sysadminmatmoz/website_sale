# -*- coding: utf-8 -*-

import logging
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

    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = fields.Datetime.from_string(self.date_beg).strftime('%Yw%V')
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

    def cron_promotion_creation_check(self):
        """ Check if we have a scheduled promotion for next week. If not notify managers """
        # monday = weekday #0
        days_ahead = 7 - date.today().weekday()
        next_monday = date.today() + timedelta(days_ahead)
        next_week_name = next_monday.strftime('%Yw%V')
        promo_count = self.env['product.promotion'].search([
            ('state', '=', 'next'),
            ('name', '=', next_week_name) ])
        res = 'PASSED'
        if promo_count == 0:
            res = 'FAILED'
            user_manager_ids = self['hr.employee'].search([('manager', '=', True)])
            for manager in user_manager_ids:
                mail_mail = self.env['mail.mail']
                mail_txt = _("Please remember to create a promotion for week {}".format(next_week_name))
                mail_id = mail_mail.create({
                                    'body_html': mail_txt,
                                    'subject': 'Odoo Promotion Creation Notification',
                                    'email_to': manager.work_email,
                                    'email_from': "odoo@abakusitsolutions.eu",
                                    'state': 'outgoing',
                                    'type': 'email',
                                    'auto_delete': True,
                                })
                mail_mail.send([mail_id])

        _logger.debug('Promotion Creation Check: week {} - {}'.format(next_week_name, res))

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
