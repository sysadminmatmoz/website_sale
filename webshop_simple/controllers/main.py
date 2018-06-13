# -*- coding: utf-8 -*-
import logging

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import PPR

_logger = logging.getLogger(__name__)


class WebsiteSale(http.Controller):

    def get_attribute_value_ids(self, product):
        """ list of selectable attributes of a product
        :return: list of product variant description
           (variant id, [visible attribute ids], variant price, variant sale price)
        """
        # product attributes with at least two choices
        quantity = product._context.get('quantity') or 1
        product = product.with_context(quantity=quantity)

        visible_attrs_ids = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped('attribute_id').ids
        to_currency = request.website.get_current_pricelist().currency_id
        attribute_value_ids = []
        for variant in product.product_variant_ids:
            if to_currency != product.currency_id:
                price = variant.currency_id.compute(variant.website_public_price, to_currency) / quantity
            else:
                price = variant.website_public_price / quantity
            visible_attribute_ids = [v.id for v in variant.attribute_value_ids if v.attribute_id.id in visible_attrs_ids]
            attribute_value_ids.append([variant.id, visible_attribute_ids, variant.website_price, price])
        return attribute_value_ids

    def _get_search_domain(self, search, category, attrib_values):
        domain = request.website.sale_product_domain()
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch)]

        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]

        return domain

    # ------------------------------------------------------
    # Simple category grid page
    # ------------------------------------------------------
    @http.route([
        '/shop/simple',
        '/shop/simple/category/<model("product.public.category"):category>'
    ], type='http', auth="public", website=True)
    def shop_simple_category(self, category=None, search='', **kwargs):

        if not category:
            categories = request.env['product.public.category'].search([('parent_id', '=', False)])

            values = {
                'categories': categories,
                'rows': PPR,
                'post': kwargs,
                'escape': lambda x: x.replace("'", r"\'")
            }

            return request.render("webshop_simple.shop_simple", values)

        category_context = dict(request.env.context,
                                active_id=category.id,
                                partner=request.env.user.partner_id)

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attrib_set = set([v[1] for v in attrib_values])

        # Get all products from this category
        Product = request.env['product.template']
        domain = self._get_search_domain(search, category, attrib_values)
        product_count = Product.search_count(domain)
        products = Product.search(domain)

        keep = QueryURL('/shop', category=category and category.id, search=search, attrib=attrib_list)
        pricelist_context = dict(request.env.context)
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)

        values = {
            'search': search,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'keep': keep,
            'main_object': category,
            'category': category,
            'product_count': product_count,
            'products': products,
            'compute_currency': compute_currency,
            'get_attribute_value_ids': self.get_attribute_value_ids,
        }
        return request.render("webshop_simple.category", values)
