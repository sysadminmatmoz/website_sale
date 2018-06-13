# -*- coding: utf-8 -*-
{
    'name': "Category bread type",

    'summary': "Bread type management",

    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'eCommerce',
    'version': '10.0.1.0.0',

    'depends': [
        'website_sale'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/product_category_view.xml',
        'views/product_view.xml',
        'views/breadtype.xml',
    ],

    'installable': True
}
