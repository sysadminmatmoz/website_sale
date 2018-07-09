# -*- coding: utf-8 -*-
{
    'name': "Birthday promotion discount",
    'summary': "Give a promotion on user birthday",
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Website',
    'version': '10.0.1.0.0',
    'depends': [
        'website_sale',
        'website_sale_birthday_ddmm',
    ],
    'data': [
        'data/ir_cron.xml',
        'data/birthday_email_template.xml',

        'views/portal_template.xml',
        'views/res_company.xml',
        'views/res_partner.xml',
    ],
    'installable': True
}
