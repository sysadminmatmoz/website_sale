# -*- coding: utf-8 -*-
{
    'name': "eCommerce 'Rich Description' on Product",

    'summary': """
    """,

    'description': """
        eCommerce 'Rich Description' on Product"
        
        This module adds the 'rich description' on the product pages if it exists on the product.
        
        This module has been developed by Valentin THIRION @ AbAKUS it-solutions.
    """,

    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Sale',
    'version': '11.0.1.0',

    'depends': [
        'website_sale',
        'product_full_description',
    ],

    'data': [
        'views/website_templates.xml',
    ],

    'installable': True
}
