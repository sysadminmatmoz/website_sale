# -*- coding: utf-8 -*-
{
    'name': "Category size tag",

    'summary': "Size tag management",
    'description': "Size tag management",

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
        'views/sizetag.xml',
    ],

    'installable': True
}
