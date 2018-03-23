# -*- coding: utf-8 -*-
{
    'name': "eCommerce 'No-Price' Management",

    'summary': """
    """,

    'description': """
        eCommerce 'No-Price' Management
        
        This module changes the normal behaviour of the ecommerce website to a 'ask for quotation' management.

    Basically, it removes prices, payment methods and so on.
    But leaves the process normal except that the orders have to be sent by the internal Odoo users to the customer who creates the quote request.
        
        This module has been developed by Valentin THIRION @ AbAKUS it-solutions.
    """,

    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Sale',
    'version': '10.0.1.0',

    'depends': [
        'website_sale'
    ],

    'data': [
        'views/sale_order.xml',
        'views/website_templates.xml',
    ],

    'installable': True
}
