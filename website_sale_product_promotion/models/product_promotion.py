# -*- coding: utf-8 -*-

from datetime import date
from datetime import timedelta
from odoo import api, fields, models, _


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
        ('next', _('Next')),
        ('curr', _('Current')),
        ('closed', _('Closed'))], string='Status', default='next', required=True)

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
            fields.Datetime.from_string(self.date_beg).strftime('%Y%-%m-%d'),
            fields.Datetime.from_string(self.date_end).strftime('%Y%-%m-%d'))

    @api.onchange('date_beg')
    def _compute_date_end(self):
        self.date_end = (fields.Date.from_string(self.date_beg) + timedelta(weeks=1)).strftime('%Y-%m-%d')
