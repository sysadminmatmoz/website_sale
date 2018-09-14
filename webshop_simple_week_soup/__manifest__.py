# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
{
    'name': "Week Soup for Simple Webshop",
    'summary': "Mail Soup of The Week",
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
        'data/week_soup_email_template.xml',

        'views/res_company.xml',
    ],
    'installable': True
}
