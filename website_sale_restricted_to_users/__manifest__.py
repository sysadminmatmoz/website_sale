# -*- coding: utf-8 -*-
{
    'name': "eCommerce Restricted to registered users",

    'summary': """
    """,

    'description': """
        eCommerce Restricted to registered users
        
        This module will check for each page of the /shop module if the current user is registred.
        If yes, it will present the correct pages, if not it will show a page that suggets the user to contact the company to have an account.
        
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
        'views/website_templates.xml',
    ],

    'installable': True
}
