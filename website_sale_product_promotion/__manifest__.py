# -*- coding: utf-8 -*-
{
    'name': "Web Shop Product Promotion",
    'summary': "Promote two products from web shop",
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Sale',
    'version': '10.0.2.0.0',
    'depends': [
        'base',
        'mail',
        'webshop_simple',
    ],
    'data': [
        'views/portal_template.xml',
        'views/res_partner.xml',
        'views/product_view.xml',
        'views/sale_order_views.xml',

        'data/promotion_mail.xml',
        'data/ir_cron.xml',

        'security/ir.model.access.csv',
    ],
    'installable': True
}
