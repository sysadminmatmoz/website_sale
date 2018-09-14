# -*- coding: utf-8 -*-
{
    'name': "Week Menu for Simple Webshop",
    'summary': "Mail Menu of The Week",
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Website',
    'version': '10.0.1.0.0',
    'depends': [
        'webshop_simple_open_hours',
        'webshop_simple',
    ],
    'data': [
        'data/ir_cron.xml',
        'data/week_menu_email_template.xml',

        'views/res_partner.xml',
        'views/res_company.xml',
    ],
    'installable': True
}
