# coding: utf-8
# -*- coding: utf-8 -*-
import datetime

import requests
from odoo.addons.payment_cybersource.controllers.main import CyberSourceController
from .cybersource_request import CyberSourceAPI
from ..models import cybersource_request
from random import randrange
import suds
from suds.client import Client
from suds.sax.attribute import Attribute
from suds.sax.element import Element
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
import logging
import time
from odoo import _, api, fields, models
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare, float_repr
from odoo.exceptions import UserError
from odoo.http import request


def get_sale_order_data(sale_order_id):
    sale_order = request.env['sale.order'].sudo().browse(sale_order_id)
    values = {
        'grandTotalAmount': sale_order.amount_total,
    }
    return values
    print("------------sale--->", values)


def get_bill_to_data(partner_id):
    partner = request.env['res.partner'].sudo().browse(partner_id)
    values = {
        'firstName': partner.name,
        'title': partner.title,
        'email': partner.email,
        'city': partner.city,
        'street': partner.street,
        'street2': partner.street2,
        'postalCode': partner.zip,
        'country': partner.country_id.name,
        'company': partner.company_id.name,
        'phone': partner.phone,
        'customer_id': partner.id
    }
    return values
    print("----------bill------->", values)


def get_card_data(card):
    values = {
        'fullName': card.get('cc_holder_name'),
        'accountNumber': card.get('cc_number'),
        'cc_expiry': card.get('cc_expiry'),
        'cvNumber': card.get('cvNumber')
    }
    return values


class PaymentAcquirerCyberSource(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[
        ('cybersource', 'CyberSource')], ondelete={'cybersource': 'set default'})
    cybersource_login = fields.Char(string='API Login Id', required_if_provider='cybersource', groups='base.group_user')
    cybersource_transaction_key = fields.Char(string='API Transaction Key', required_if_provider='cybersource',
                                              groups='base.group_user')

    def _get_feature_support(self):
        res = super(PaymentAcquirerCyberSource, self)._get_feature_support()
        res['tokenize'].append('cybersource')
        return res

    def _get_cybersource_urls(self, environment):
        """ Authorize URLs """
        if environment == 'prod':
            return {'cybersource_form_url': 'https://apitest.cybersource.com/pts/v2/payments'}
        else:
            return {'cybersource_form_url': 'https://apitest.cybersource.com/pts/v2/payments'}

    def cybersource_form_generate_values(self, values):
        self.ensure_one()
        print("-----------generate-------", cybersource_form_generate_values)
        # State code is only supported in US, use state name by default
        state = values['partner_state'].name if values.get('partner_state') else ''
        if values.get('partner_country') and values.get('partner_country') == self.env.ref('base.us', False):
            state = values['partner_state'].code if values.get('partner_state') else ''
        billing_state = values['billing_partner_state'].name if values.get('billing_partner_state') else ''
        if values.get('billing_partner_country') and values.get('billing_partner_country') == self.env.ref('base.us',
                                                                                                           False):
            billing_state = values['billing_partner_state'].code if values.get('billing_partner_state') else ''

        base_url = self.get_base_url()
        authorize_tx_values = dict(values)
        print("\n\n\n\n return")
        print(authorize_tx_values)
        temp_authorize_tx_values = {'x_login': self.cybersource_login, 'x_amount': float_repr(values['amount'], values[
            'currency'].decimal_places if values['currency'] else 2), 'x_show_form': 'PAYMENT_FORM',
                                    'x_type': 'AUTH_CAPTURE' if not self.capture_manually else 'AUTH_ONLY',
                                    'x_method': 'CC', 'x_fp_sequence': '%s%s' % (self.id, int(time.time())),
                                    'x_version': '3.1', 'x_relay_response': 'TRUE',
                                    'x_fp_timestamp': str(int(time.time())),
                                    'x_currency_code': values['currency'] and values['currency'].name or '',
                                    'address': values.get('partner_address'), 'city': values.get('partner_city'),
                                    'country': values.get('partner_country') and values.get(
                                        'partner_country').name or '', 'email': values.get('partner_email'),
                                    'zip_code': values.get('partner_zip'),
                                    'first_name': values.get('partner_first_name'),
                                    'last_name': values.get('partner_last_name'), 'phone': values.get('partner_phone'),
                                    'state': state, 'billing_address': values.get('billing_partner_address'),
                                    'billing_city': values.get('billing_partner_city'),
                                    'billing_country': values.get('billing_partner_country') and values.get(
                                        'billing_partner_country').name or '',
                                    'billing_email': values.get('billing_partner_email'),
                                    'billing_zip_code': values.get('billing_partner_zip'),
                                    'billing_first_name': values.get('billing_partner_first_name'),
                                    'billing_last_name': values.get('billing_partner_last_name'),
                                    'billing_phone': values.get('billing_partner_phone'),
                                    'billing_state': billing_state,
                                    'returndata': authorize_tx_values.pop('return_url', '')}

        authorize_tx_values.update(temp_authorize_tx_values)
        return authorize_tx_values

    def cybersource_get_form_action_url(self):
        self.ensure_one()
        environment = 'prod' if self.state == 'enabled' else 'test'
        return self._get_cybersource_urls(environment)['cybersource_form_url']

    @api.model
    def cybersource_s2s_form_process(self, data):
        print("data:", data)
        values = {
            'cc_number': data.get('cc_number'),
            'cc_cvc': int(data.get('cc_cvc')),
            'cc_holder_name': data.get('cc_holder_name'),
            'cc_expiry': data.get('cc_expiry'),
            'cc_brand': data.get('cc_brand'),
            'acquirer_id': int(data.get('acquirer_id')),
            'partner_id': int(data.get('partner_id'))
        }
        pm_id = self.env['payment.token'].sudo().create(values)
        print("pm id: ", pm_id)
        return pm_id


class TxCyberSource(models.Model):
    _inherit = 'payment.transaction'

    _cybersource_valid_tx_status = 100
    _cybersource_pending_tx_status = 4
    _cybersource_cancel_tx_status = 2
    _cybersource_tx_status = 3

    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------

    def cybersource_s2s_do_transaction(self):
        self.ensure_one()
        print("\n\n\n\n\n s2 ")

        if not self.payment_token_id.cybersource_profile:
            print("if")
            raise UserError(_('Invalid token found: the CyberSource profile is missing.'
                              'Please make sure the token has a valid acquirer reference.'))

        acquirer = self.env['payment.acquirer'].search([('name', '=', 'CyberSource')])
        sale_order_id = int(request.session.get('sale_order_id'))
        print("sa")
        sale_order_data = get_sale_order_data(sale_order_id)
        bill_to_data = get_bill_to_data(int(request.session.get('partner_id')))
        card_data = get_card_data(request.session.get('card_data'))

        # call Api
        req = CyberSourceAPI(acquirer)
        req.create_headers()
        req.billing_info(bill_to_data)
        req.payment_amount(sale_order_data)
        req.set_card_info(card_data)
        response = req.cybersource_request()
        print("\n\n\n\n\n\nresponse:", response)

        return self._cybersource_s2s_validate_tree(response)

    def _cybersource_s2s_validate_tree(self, tree):
        return self._cybersource_s2s_validate(tree)

    def _cybersource_s2s_validate(self, tree):
        if self.state == 'done':
            _logger.warning('CyberSource: trying to validate an already validated tx (ref %s)' % self.reference)
            return True
        status_code = tree.get('reasonCode', 0)
        if status_code == self._cybersource_valid_tx_status:
            tx_id = Client.dict(tree.get('ccAuthReply')).get('reconciliationID')
            self.write({
                'acquirer_reference': tx_id,
                'date': fields.Datetime.now(),
            })
            self._set_transaction_done()
            return True
        else:
            self.write({'acquirer_reference': ""})
            self._set_transaction_cancel()
            raise UserError(_('API CALL REJECTED. \nTRANSACTION CANCELLED. \nERROR CODE: %s, \nERROR DETAILS: %s!' % (
                status_code, cybersource_request.CYBERSOURCE_RESPONSES.get(str(status_code)))))


class PaymentToken(models.Model):
    _inherit = 'payment.token'

    cybersource_profile = fields.Char(string='cybersource.net Profile ID', help='This contains the unique reference '
                                                                                'for this partner/payment token combination in the Authorize.net backend')
    provider = fields.Selection(string='Provider', related='acquirer_id.provider', readonly=False)
    save_token = fields.Selection(string='Save Cards', related='acquirer_id.save_token', readonly=False)

    @api.model
    def cybersource_create(self, values):
        if values.get('cc_number') and values.get('acquirer_id'):
            acquirer = self.env['payment.acquirer'].browse(values['acquirer_id'])
            partner = self.env['res.partner'].browse(values['partner_id'])
            alias = 'ODOO-NEW-ALIAS-%s' % time.time()
            profile = 'cs-%s' % time.time()
            request.session.update({
                'card_data': {
                    'cc_number': values.get('cc_number'),
                    'cc_holder_name': values.get('cc_holder_name'),
                    'cc_expiry': values.get('cc_expiry'),
                    'cvNumber': values.get('cc_cvc'),
                    'cc_brand': values.get('cc_brand'),
                },
                'partner_id': values.get('partner_id')
            })
            return {
                'cybersource_profile': profile,
                'acquirer_ref': alias,
                'verified': True,
                'name': 'XXXXXXXXXXXX%s - %s' % (values['cc_number'][-4:], values['cc_holder_name'])
            }
        else:
            return values
