# -*- coding: utf-8 -*-
#
import logging
from pprint import pformat
from odoo import models, api, fields, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _get_extra_line_description(self, order_id, product_id, breadtype=None, sizetag=None, sides=None):
        extra_name = ""

        order = self.sudo().browse(order_id)
        product_context = dict(self.env.context)
        product_context.setdefault('lang', order.partner_id.lang)
        main_product = self.env['product.product'].with_context(product_context).browse(product_id)
        if breadtype:
            for bl in main_product.breadtype_line_ids:
                if int(bl.id) == int(breadtype):
                    extra_name += u"\nBread: %s" % bl.breadtype_id.name
        if sizetag:
            for sl in main_product.sizetags_line_ids:
                if int(sl.id) == int(sizetag):
                    extra_name += u"\nSize: %s" % sl.sizetag_id.name
        if sides and len(sides) > 0:
            for side in sides:
                side_product = self.env['product.template'].search([('id', '=', int(side))])
                if side_product:
                    extra_name += "\nSide: %s" % side_product.display_name
                else:
                    # TODO: raise error
                    _logger.debug(u"ABAKUS**: can_t find side product_id:{}".format(int(side)))
                    return None
        return extra_name

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, attributes=None, **kwargs):
        """ Add or set product quantity, add_qty can be negative """
        self.ensure_one()
        SaleOrderLineSudo = self.env['sale.order.line'].sudo()

        try:
            if add_qty:
                add_qty = float(add_qty)
        except ValueError:
            add_qty = 1
        try:
            if set_qty:
                set_qty = float(set_qty)
        except ValueError:
            set_qty = 0
        quantity = 0
        order_line = False
        if self.state != 'draft':
            request.session['sale_order_id'] = None
            raise UserError(_('It is forbidden to modify a sales order which is not in draft status'))
        if line_id is not False:
            if line_id is not None:
                order_lines = self._cart_find_product_line(product_id, line_id, **kwargs)
                order_line = order_lines and order_lines[0]

        # Create line if no line with product_id can be located
        if not order_line:
            values = self._website_product_id_change(self.id, product_id, qty=1)
            # Take our custom field into account
            breadtype = None
            if 'breadtype' in kwargs:
                breadtype = kwargs['breadtype']
            sizetag = None
            if 'sizetag' in kwargs:
                sizetag = kwargs['sizetag']
            sides = []
            if 'sides' in kwargs:
                # we can not turn them into attributes because it will create variants
                sides = kwargs['sides']
            values['breadtype'] = breadtype
            values['sizetag'] = sizetag
            # make sur we create sides properly
            values['sides'] = [(6, 0, sides)]
            values['name'] = self._get_line_description(self.id, product_id, attributes=attributes)
            # Extra infos
            values['name'] += self._get_extra_line_description(self.id, product_id,
                                                               breadtype=breadtype, sizetag=sizetag, sides=sides)
            if 'has_birthday_gift' in kwargs and kwargs['has_birthday_gift']:
                # This is a birthday gift so we give it for free by setting discount to 100 %
                values['discount'] = 100
            # set default alias
            if 'alias' not in values:
                values['alias'] = self.partner_id.name.split(' ', 1)[0]
            order_line = SaleOrderLineSudo.create(values)

            try:
                order_line._compute_tax_id()
            except ValidationError as e:
                # The validation may occur in backend (eg: taxcloud) but should fail silently in frontend
                _logger.debug("ValidationError occurs during tax compute. %s" % (e))
            if add_qty:
                add_qty -= 1

        # compute new quantity
        if set_qty:
            quantity = set_qty
        elif add_qty is not None:
            quantity = order_line.product_uom_qty + (add_qty or 0)

        # Remove zero of negative lines
        if quantity <= 0:
            order_line.unlink()
        else:
            # update line
            values = self._website_product_id_change(self.id, product_id, qty=quantity)
            if self.pricelist_id.discount_policy == 'with_discount' and not self.env.context.get('fixed_price'):
                order = self.sudo().browse(self.id)
                product_context = dict(self.env.context)
                product_context.setdefault('lang', order.partner_id.lang)
                product_context.update({
                    'partner': order.partner_id.id,
                    'quantity': quantity,
                    'date': order.date_order,
                    'pricelist': order.pricelist_id.id,
                })
                product = self.env['product.product'].with_context(product_context).browse(product_id)
                values['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
                    order_line._get_display_price(product),
                    order_line.product_id.taxes_id,
                    order_line.tax_id,
                    self.company_id
                )
            order_line.write(values)

        return {'line_id': order_line.id, 'quantity': quantity}
