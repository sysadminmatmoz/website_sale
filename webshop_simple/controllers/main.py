# -*- coding: utf-8 -*-
import pytz
import logging

from pprint import pformat
from datetime import datetime, timedelta
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import PPR, WebsiteSale
from odoo.addons.website.models.website import slug

_logger = logging.getLogger(__name__)

DEFAULT_CATEGORIES = [
    "product.product_category_sandwich",
    "product.product_category_salad",
    "product.product_category_meal",
    "product.product_category_dessert",
]


class WebsiteSaleSimple(WebsiteSale):

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

    def _get_search_domain_simple(self, search, category, attrib_values):
        domain = request.website.sale_product_domain()
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', ('name', 'ilike', srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch)]

        if category:
            # Note that we use internal categories instead of public (public_categ_ids)
            if category.id == request.env.ref('product.product_category_meal').id:
                # include todays special
                company = request.env.user.sudo().company_id
                special_product_ids = []
                # today's special
                today_special_product_id = company.get_named_day_product()
                if today_special_product_id:
                    special_product_ids.append(today_special_product_id.product_tmpl_id.id)
                # today's soup
                today_special_soup_id = company.get_named_day_soup()
                if today_special_soup_id:
                    special_product_ids.append(today_special_soup_id.product_tmpl_id.id)
                if len(special_product_ids) > 0:
                    domain += ['|', ('id', 'in', special_product_ids), ('categ_id', '=', category.id)]
                else:
                    domain += [('categ_id', '=', category.id)]
            else:
                domain += [('categ_id', '=', category.id)]
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
    # Simple Web Shop landing page
    # ------------------------------------------------------
    @http.route(['/shop/simple'], type='http', auth="public", website=True)
    def shop_simple(self, category=None, search='', **kwargs):
        simple_categories = ('sandwich', 'salad', 'meal', 'dessert')
        # Build the /shop/simple endpoint using internal categories
        categories = {x: request.env.ref('product.product_category_' + x).id for x in simple_categories}

        values = {
            'categories': categories,
            'rows': PPR,
            'post': kwargs,
            'escape': lambda x: x.replace("'", r"\'")
        }
        return request.render("webshop_simple.shop_simple", values)

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        """ We don't want this endpoint to be accessible anymore.
            We can't no longer do a smart redirect based on category since we use internal ones in
            /shop/simple.
         """
        return request.redirect('/shop/simple')

    # ------------------------------------------------------
    # Simple Web Shop category page
    # ------------------------------------------------------
    @http.route(['/shop/simple/category/<model("product.category"):category>'],
                type='http', auth="public", website=True)
    def shop_simple_category(self, category=None, search='', **kwargs):
        """ We display results from 5 top categories only
        Work categories like product_category_todaysspecial should not be accessible through
        this endpoint
        """
        if category is None:
            # we forbid call with not category
            return request.redirect('/shop/simple')
        category_ids = [request.env.ref(x).id for x in DEFAULT_CATEGORIES]
        if category.id not in category_ids:
            # we forbid call to non simple categories
            return request.redirect('/shop/simple')

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attrib_set = set([v[1] for v in attrib_values])

        # Get all products from this category that are base_sides
        domain = self._get_search_domain_simple(search, category, attrib_values)
        domain += [('active', '=', True)]
        products = request.env['product.template'].search(domain)

        # set the default product to display
        product_count = len(products)
        if product_count == 0:
            return request.redirect('/shop/simple')

        pricelist_context = dict(request.env.context)
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])
        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)
        company = request.env.user.sudo().company_id

        values = {
            'search': search,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'company': company,
            'main_object': category,
            'category': category,
            'product_count': product_count,
            'products': products,
            'compute_currency': compute_currency,
            'get_attribute_value_ids': self.get_attribute_value_ids,
        }
        if category.has_base_products:
            return self.shop_simple_category_render("webshop_simple.category", values)
        else:
            return self.shop_simple_category_render("webshop_simple.category_product", values)

    @staticmethod
    def shop_simple_category_render(page, values):
        return request.render(page, values)

    # ------------------------------------------------------
    # Simple Web Shop category product page
    # ------------------------------------------------------
    @http.route(['/shop/simple/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def shop_simple_category_product(self, product, category='', search='', **kwargs):
        # Build the /shop/simple/category/  endpoint
        product_context = dict(request.env.context,
                               active_id=product.id,
                               partner=request.env.user.partner_id)
        ProductCategory = request.env['product.category']
        if category:
            category = ProductCategory.browse(int(category)).exists()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attrib_set = set([v[1] for v in attrib_values])

        # Get all products from this category that are base_sides
        domain = self._get_search_domain_simple(search, category, attrib_values)
        products = request.env['product.template'].search(domain)
        product_count = len(products)

        # Get all product sides if any
        sides = []
        for accessory in product.accessory_product_ids:
            sides.extend(request.env['product.template'].search([('id', '=', accessory.product_tmpl_id.id)]))
        sides_count = len(sides)

        keep = QueryURL('/shop/simple', category=category and category.id, search=search, attrib=attrib_list)
        pricelist_context = dict(request.env.context)
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)
        company = request.env.user.sudo().company_id

        values = {
            'search': search,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'keep': keep,
            'company': company,
            'main_object': category,
            'category': category,
            'product_count': product_count,
            'products': products,
            'product': product,
            'sides_count': sides_count,
            'sides': sides,
            'compute_currency': compute_currency,
            'get_attribute_value_ids': self.get_attribute_value_ids,
        }
        return request.render("webshop_simple.category_product", values)

    # ------------------------------------------------------
    # Handle cart
    # ------------------------------------------------------
    def _filter_attributes(self, **kw):
        return {k: v for k, v in kw.items() if "attribute" in k}

    @http.route(['/shop/cart/update'],
                type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        breadtype = None
        if 'breadtype_' + str(product_id) in kw:
            breadtype = kw['breadtype_' + str(product_id)]
        sizetag = None
        if 'sizetag_' + str(product_id) in kw:
            sizetag = kw['sizetag_' + str(product_id)]
        sides = []
        for key in kw:
            if key.startswith("sides-" + str(product_id) + '-'):
                sides.append(int(kw[key]))

        # check if it's a birthday gift
        has_birthday_gift = False
        company = request.env.user.sudo().company_id
        if int(product_id) == company.birthday_promotion_product_id.id:
            if request.env.user._is_portal():
                if request.env.user._has_birthday_gift():
                    has_birthday_gift = True
        _logger.debug("ABAKUS: Add to cart product_id={}".format(int(product_id)))
        request.website.sale_get_order(force_create=1)._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            attributes=self._filter_attributes(**kw),
            sizetag=sizetag,
            breadtype=breadtype,
            sides=sides,
            has_birthday_gift=has_birthday_gift,
        )
        return request.redirect("/shop/cart")

    @http.route(['/shop/cart/update_alias_json'],
                type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_alias_json(self, product_id, line_id, alias, **kw):
        """ Custom endpoint to update SOL label """
        order = request.website.sale_get_order()
        order_lines = order._cart_find_product_line(product_id, line_id, **kw)
        order_line = order_lines and order_lines[0]
        values = {
            'alias': alias
        }
        order_line.write(values)
        return {}

    # When everything goes on the app side we go through this code
    @http.route(['/shop/confirmation'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        """ Let set the SO delivery date here since we are now sure SO is paid """
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            company = order.company_id
            now = datetime.now(pytz.timezone(company.openhours_tz))
            position = company.is_between_open_hours(now)
            values = {'delivery_date': now.strftime("%Y-%m-%d")}
            if position == 1:
                values['delivery_date'] = (now + timedelta(days=1)).strftime("%Y-%m-%d")
            order.write(values)
        return super(WebsiteSaleSimple, self).payment_confirmation(**post)

    # If Somehow the app crashes we can't reach confirmation so we have to set the delivery date here
    @http.route('/shop/payment/validate', type='http', auth="public", website=True)
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        if transaction_id is None:
            tx = request.website.sale_get_transaction()
        else:
            tx = request.env['payment.transaction'].browse(transaction_id)

        if sale_order_id is None:
            order = request.website.sale_get_order()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')

        if order and tx:
            company = order.company_id
            now = datetime.now(pytz.timezone(company.openhours_tz))
            position = company.is_between_open_hours(now)
            values = {'delivery_date': now.strftime("%Y-%m-%d")}
            if position == 1:
                values['delivery_date'] = (now + timedelta(days=1)).strftime("%Y-%m-%d")
            order.write(values)

        return super(WebsiteSaleSimple, self).payment_validate(transaction_id, sale_order_id, **post)

    # If total is = 0 we do not allow checkout
    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        order = request.website.sale_get_order()
        if order and order.amount_total == 0:
            return request.redirect('/shop/cart')
        else:
            return super(WebsiteSaleSimple, self).checkout(**post)
