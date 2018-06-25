# -*- coding: utf-8 -*-
{
    'name': "Webshop Simplified",
    'summary': "Simple categories based landing page",
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Website',
    'version': '10.0.1.0.0',
    'depends': [
        'website_sale',
        'website_sale_category_bread',
        'website_sale_category_size',
    ],
    'data': [
        'data/simple_categories.xml',

        'views/templates.xml',
    ],
    'installable': True
}
