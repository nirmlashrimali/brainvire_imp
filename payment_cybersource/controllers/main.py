  # -*- coding: utf-8 -*-

from ..models import cybersource_request as cr
import pprint
import logging
from werkzeug import urls, utils

from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class CyberSourceController(http.Controller):
    _return_url = '/payment/cybersource/return/'
    _cancel_url = '/payment/cybersource/cancel/'

    @http.route([
        '/payment/cybersource/return/',
        '/payment/cybersource/cancel/',
    ], type='http', auth='public', csrf=False)
    def cybersource_form_feedback(self, **post):
        print("Calling Feedback for transaction")
        _logger.info('Cybersource: entering form_feedback with post data %s', pprint.pformat(post))
        if post:
            request.env['payment.transaction'].sudo().form_feedback(post, 'cybersource')
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        print("base url", base_url)
        # Authorize.Net is expecting a response to the POST sent by their server.
        # This response is in the form of a URL that Authorize.Net will pass on to the
        # client's browser to redirect them to the desired location need javascript.
        return werkzeug.utils.redirect("/payment/process")

    @http.route(['/payment/cybersource/s2s/create_json_3ds'], type='json', auth='public', csrf=False)
    def cybersource_s2s_create_json_3ds(self, verify_validity=False, **kwargs):
        print("\n\n\n\n\n\n\n\n\n ->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(kwargs)
        token = False
        acquirer = request.env['payment.acquirer'].browse(int(kwargs.get('acquirer_id')))
        print("acqu")
        print("\n\n\n\n\n\n->>>>>>>>>>>>>>>>>")
        print(acquirer)
        partner = request.env['res.partner'].browse(int(kwargs.get('partner_id')))
        print(partner)
        try:
            if not kwargs.get('partner_id'):
                print("ig not")
                kwargs = dict(kwargs, partner_id=request.env.user.partner_id.id)
            token = acquirer.s2s_process(kwargs)
            print("token", token)
        except ValidationError as e:
            print("exce")
            message = e.args[0]
            if isinstance(message, dict) and 'missing_fields' in message:
                if request.env.user._is_public():
                    message = _("Please sign in to complete the payment.")
                    # update message if portal mode = b2b
                    if request.env['ir.config_parameter'].sudo().get_param('auth_signup.allow_uninvited',
                                                                           'False').lower() == 'false':
                        message += _(
                            " If you don't have any account, ask your salesperson to grant you a portal access. ")
                else:
                    msg = _("The transaction cannot be processed because some contact details are missing or invalid: ")
                    message = msg + ', '.join(message['missing_fields']) + '. '
                    message += _("Please complete your profile. ")

            return {
                'error': message
            }

        if not token:
            res = {
                'result': False,
            }
            return res

        res = {
            'result': True,
            'id': token.id,
            'short_name': token.short_name,
            '3d_secure': False,
            'verified': False,  # Authorize.net does a transaction type of Authorization Only
            # As Authorize.net already verify this card, we do not verify this card again.
        }
        if verify_validity != False:
            baseurl = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            params = {
                'accept_url': baseurl + '/payment/cybersource/validate/accept',
                'decline_url': baseurl + '/payment/cybersource/validate/decline',
                'exception_url': baseurl + '/payment/cybersource/validate/exception',
                'return_url': kwargs.get('return_url', baseurl)
            }
            tx = token.validate(**params)
            res['verified'] = token.verified

            if tx and tx.html_3ds:
                res['3d_secure'] = tx.html_3ds

        return res

    @http.route([
        '/payment/cybersource/validate/accept',
        '/payment/cybersource/validate/decline',
        '/payment/cybersource/validate/exception',
    ], type='http', auth='public')
    def cybersource_validation_form_feedback(self, **post):
        """ Feedback from 3d secure for a bank card validation """
        print("\n\n\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&cybersource_validation_form_feedback")
        request.env['payment.transaction'].sudo().form_feedback(post, 'ogone')
        return werkzeug.utils.redirect("/payment/process")

    @http.route(['/payment/cybersource/s2s/create_json'], type='json', auth='public', csrf=False)
    def cybersource_s2s_create_json(self, **kwargs):
        if not kwargs.get('partner_id'):
            kwargs = dict(kwargs, partner_id=request.env.user.partner_id.id)
        new_id = request.env['payment.acquirer'].browse(int(kwargs.get('acquirer_id'))).s2s_process(kwargs)
        return new_id.id

    @http.route(['/payment/cybersource/s2s/create'], type='http', auth='public')
    def cybersource_s2s_create(self, **post):
        print("\n\n cybersource_s2s_create")
        acquirer_id = int(post.get('acquirer_id'))
        acquirer = request.env['payment.acquirer'].browse(acquirer_id)
        acquirer.s2s_process(post)
        return utils.redirect("/payment/process")

    @http.route([
        '/payment/cybersource/validate/accept',
        '/payment/cybersource/validate/decline',
        '/payment/cybersource/validate/exception',
    ], type='http', auth='public')
    def cybersource_validation_form_feedback(self, **post):
        """ Feedback from 3d secure for a bank card validation """
        request.env['payment.transaction'].sudo().form_feedback(post, 'cybersource')
        return werkzeug.utils.redirect("/payment/process")
