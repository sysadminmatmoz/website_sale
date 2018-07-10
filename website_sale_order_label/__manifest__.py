# -*- coding: utf-8 -*-
{
    'name': "Website Sale Order Labels",

    'summary': "Website Sale Order Labels",

    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'eCommerce',
    'version': '10.0.1.0.0',

    'depends': [
        'website_sale',
        'webshop_simple',
    ],
    'data': [
        'views/res_company.xml',
        'reports/sale_order_label_report.xml',
    ],

    'installable': True
}
