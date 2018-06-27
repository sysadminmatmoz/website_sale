import logging
from datetime import datetime
from pprint import pformat
from odoo import models, api, fields
from odoo.http import request
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bday = fields.Integer('Birthday Day')
    bmonth = fields.Integer('Birthday Month')

    def cron_birthday_promotion_mailing(self):
        partner_obj = self.env['res.partner']
        mail_mail = self.env['mail.mail']
        mail_ids = []
        today = datetime.datetime.now()
        par_id = partner_obj.search([
            ('active', '=', True),
            ('bday', '=', int(today.strftime('%d'))), ('bmonth', '=', int(today.strftime('%m')))])
        if par_id:
            try:
                for val in partner_obj.browse(par_id):
                    email_to = val.email
                    name = val.name
                    subject = "Birthday Promotion"
                    body = _("Hello %s,\n" %(name))
                    body += _("\tWish you Happy Birthday\n")
                    footer = _("Kind regards.\n")
                    footer += _("%s\n\n" % val.company_id.name)
                    mail_ids.append(mail_mail.create({
                        'email_to': email_to,
                        'subject': subject,
                        'body_html': '<pre><span class="inner-pre" style="font-size: 15px">%s<br>%s</span></pre>' % (body, footer)
                     }, context=None))
                    mail_mail.send(mail_ids, context=None)
            except Exception, e:
                print "Exception", e
        return None

    @api.multi
    def cron_promotion_mailing(self):
        """ Send mass mailing to all registered portal user with the right flag on """
        template = self.env.ref('website_sale_birthday_promotion.email_template_user_birthday')
        for record in self:
            _logger.debug("ABAKUS: Birthday omotion email sent")
            self.env['mail.template'].browse(template.id).send_mail(record.id)
        return
