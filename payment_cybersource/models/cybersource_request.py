# -*- coding: utf-8 -*-

import logging
import requests
import json

_logger = logging.getLogger(__name__)


class CyberSourceAPI():

    AUTH_ERROR_STATUS = 3

    def __init__(self, cybersource):
        """Initiate the environment with the acquirer data.

        :param record acquirer: payment.acquirer account that will be contacted
        """
        if cybersource.state == 'test':
            self.url = 'https://apitest.authorize.net/xml/v1/request.api'
        else:
            self.url = 'https://api.authorize.net/xml/v1/request.api'

        self.state = cybersource.state
        self.name = cybersource.cybersource_login
        self.transaction_key = cybersource.cybersource_transaction_key

    def _cybersource_request(self, data):
        print("\n\n\n\n\n\n\n---------cybersource_request--------\n\n\n\n")
        _logger.info('_authorize_request: Sending values to URL %s, values:\n%s', self.url, data)
        print("\n\n\n\n\n-<<<<<<<<<<<<<<<<<<<<<<<<")
        resp = requests.post(self.url, json.dumps(data))
        resp.raise_for_status()
        resp = json.loads(resp.content)
        _logger.info("_authorize_request: Received response:\n%s", resp)
        messages = resp.get('messages')
        if messages and messages.get('resultCode') == 'Error':
            return {
                'err_code': messages.get('message')[0].get('code'),
                'err_msg': messages.get('message')[0].get('text')
            }

        return resp

    # def create_customer_profile(self, partner, opaqueData):
    #     print("\n\n\n\n\n\n\n---------create_customer_profile--------\n\n\n\n")
    #     """Create a payment and customer profile in the Authorize.net backend.

    #     Creates a customer profile for the partner/credit card combination and links
    #     a corresponding payment profile to it. Note that a single partner in the Odoo
    #     database can have multiple customer profiles in Authorize.net (i.e. a customer
    #     profile is created for every res.partner/payment.token couple).

    #     :param record partner: the res.partner record of the customer
    #     :param str cardnumber: cardnumber in string format (numbers only, no separator)
    #     :param str expiration_date: expiration date in 'YYYY-MM' string format
    #     :param str card_code: three- or four-digit verification number

    #     :return: a dict containing the profile_id and payment_profile_id of the
    #              newly created customer profile and payment profile
    #     :rtype: dict
    #     """
    #     values = {
    #         'createCustomerProfileRequest': {
    #             'merchantAuthentication': {
    #                 'name': self.name,
    #                 'transactionKey': self.cybersource_transaction_key
    #             },
    #             'profile': {
    #                 'description': ('ODOO-%s-%s' % (partner.id, uuid4().hex[:8]))[:20],
    #                 'email': partner.email or '',
    #                 'paymentProfiles': {
    #                     'customerType': 'business' if partner.is_company else 'individual',
    #                     'billTo': {
    #                         'firstName': '' if partner.is_company else _partner_split_name(partner.name)[0],
    #                         'lastName':  _partner_split_name(partner.name)[1],
    #                         'address': (partner.street or '' + (partner.street2 if partner.street2 else '')) or None,
    #                         'city': partner.city,
    #                         'state': partner.state_id.name or None,
    #                         'zip': partner.zip or '',
    #                         'country': partner.country_id.name or None,
    #                         'phoneNumber': partner.phone or '',
    #                     },
    #                     'payment': {
    #                         'opaqueData': {
    #                             'dataDescriptor': opaqueData.get('dataDescriptor'),
    #                             'dataValue': opaqueData.get('dataValue')
    #                         }
    #                     }
    #                 }
    #             },
    #             'validationMode': 'liveMode' if self.state == 'enabled' else 'testMode'
    #         }
    #     }

    #     response = self._cybersource_request(values)

    #     if response and response.get('err_code'):
    #         raise UserError(_(
    #             "CyberSource Error:\nCode: %s\nMessage: %s",
    #             response.get('err_code'), response.get('err_msg'),
    #         ))

    #     return {
    #         'profile_id': response.get('customerProfileId'),
    #         'payment_profile_id': response.get('customerPaymentProfileIdList')[0]
    #     }

    # def create_customer_profile_from_tx(self, partner, transaction_id):
    #     print("\n\n\n\n\n\n\n---------create_customer_profile_from_tx--------\n\n\n\n")
    #     """Create an Auth.net payment/customer profile from an existing transaction.

    #     Creates a customer profile for the partner/credit card combination and links
    #     a corresponding payment profile to it. Note that a single partner in the Odoo
    #     database can have multiple customer profiles in Authorize.net (i.e. a customer
    #     profile is created for every res.partner/payment.token couple).

    #     Note that this function makes 2 calls to the authorize api, since we need to
    #     obtain a partial cardnumber to generate a meaningful payment.token name.

    #     :param record partner: the res.partner record of the customer
    #     :param str transaction_id: id of the authorized transaction in the
    #                                Authorize.net backend

    #     :return: a dict containing the profile_id and payment_profile_id of the
    #              newly created customer profile and payment profile as well as the
    #              last digits of the card number
    #     :rtype: dict
    #     """
    #     values = {
    #         'createCustomerProfileFromTransactionRequest': {
    #             "merchantAuthentication": {
    #                 "name": self.name,
    #                 "transactionKey": self.cybersource_transaction_key
    #             },
    #             'transId': transaction_id,
    #             'customer': {
    #                 'merchantCustomerId': ('ODOO-%s-%s' % (partner.id, uuid4().hex[:8]))[:20],
    #                 'email': partner.email or ''
    #             }
    #         }
    #     }

    #     response = self._cybersource_request(values)

    #     if not response.get('customerProfileId'):
    #         _logger.warning(
    #             'Unable to create customer payment profile, data missing from transaction. Transaction_id: %s - Partner_id: %s'
    #             % (transaction_id, partner)
    #         )
    #         return False

    #     res = {
    #         'profile_id': response.get('customerProfileId'),
    #         'payment_profile_id': response.get('customerPaymentProfileIdList')[0]
    #     }

    #     values = {
    #         'getCustomerPaymentProfileRequest': {
    #             "merchantAuthentication": {
    #                 "name": self.name,
    #                 "transactionKey": self.cybersource_transaction_key
    #             },
    #             'customerProfileId': res['profile_id'],
    #             'customerPaymentProfileId': res['payment_profile_id'],
    #         }
    #     }

    #     response = self._authorize_request(values)

    #     res['name'] = response.get('paymentProfile', {}).get('payment', {}).get('creditCard', {}).get('cardNumber')
    #     return res
    
    # # Transaction management
    # def auth_and_capture(self, token, amount, reference):
    #     """Authorize and capture a payment for the given amount.

    #     Authorize and immediately capture a payment for the given payment.token
    #     record for the specified amount with reference as communication.

    #     :param record token: the payment.token record that must be charged
    #     :param str amount: transaction amount (up to 15 digits with decimal point)
    #     :param str reference: used as "invoiceNumber" in the Authorize.net backend

    #     :return: a dict containing the response code, transaction id and transaction type
    #     :rtype: dict
    #     """
    #     values = {
    #         'createTransactionRequest': {
    #             "merchantAuthentication": {
    #                 "name": self.name,
    #                 "transactionKey": self.cybersource_transaction_key
    #             },
    #             'transactionRequest': {
    #                 'transactionType': 'authCaptureTransaction',
    #                 'amount': str(amount),
    #                 'profile': {
    #                     'customerProfileId': token.cybersource_profile,
    #                     'paymentProfile': {
    #                         'paymentProfileId': token.acquirer_ref,
    #                     }
    #                 },
    #                 'order': {
    #                     'invoiceNumber': reference[:20],
    #                     'description': reference[:255],
    #                 }
    #             }

    #         }
    #     }
    #     response = self._cybersource_request(values)
    #     print("----------------->",response)

    #     if response and response.get('err_code'):
    #         return {
    #             'x_response_code': self.AUTH_ERROR_STATUS,
    #             'x_response_reason_text': response.get('err_msg')
    #         }

    #     result = {
    #         'x_response_code': response.get('transactionResponse', {}).get('responseCode'),
    #         'x_trans_id': response.get('transactionResponse', {}).get('transId'),
    #         'x_type': 'auth_capture'
    #     }
    #     errors = response.get('transactionResponse', {}).get('errors')
    #     if errors:
    #         result['x_response_reason_text'] = '\n'.join([e.get('errorText') for e in errors])
    #     return result

    # def cybersource(self, token, amount, reference):
    #     """Authorize a payment for the given amount.

    #     Authorize (without capture) a payment for the given payment.token
    #     record for the specified amount with reference as communication.

    #     :param record token: the payment.token record that must be charged
    #     :param str amount: transaction amount (up to 15 digits with decimal point)
    #     :param str reference: used as "invoiceNumber" in the Authorize.net backend

    #     :return: a dict containing the response code, transaction id and transaction type
    #     :rtype: dict
    #     """
    #     values = {
    #         'createTransactionRequest': {
    #             "merchantAuthentication": {
    #                 "name": self.name,
    #                 "transactionKey": self.cybersource_transaction_key
    #             },
    #             'transactionRequest': {
    #                 'transactionType': 'authOnlyTransaction',
    #                 'amount': str(amount),
    #                 'profile': {
    #                     'customerProfileId': token.cybersource_profile,
    #                     'paymentProfile': {
    #                         'paymentProfileId': token.acquirer_ref,
    #                     }
    #                 },
    #                 'order': {
    #                     'invoiceNumber': reference[:20],
    #                     'description': reference[:255],
    #                 }
    #             }

    #         }
    #     }
    #     response = self._cybersource_request(values)

    #     if response and response.get('err_code'):
    #         return {
    #             'x_response_code': self.AUTH_ERROR_STATUS,
    #             'x_response_reason_text': response.get('err_msg')
    #         }

    #     return {
    #         'x_response_code': response.get('transactionResponse', {}).get('responseCode'),
    #         'x_trans_id': response.get('transactionResponse', {}).get('transId'),
    #         'x_type': 'auth_only'
    #     }
    
    # def capture(self, transaction_id, amount):
    #     """Capture a previously authorized payment for the given amount.

    #     Capture a previsouly authorized payment. Note that the amount is required
    #     even though we do not support partial capture.

    #     :param str transaction_id: id of the authorized transaction in the
    #                                Authorize.net backend
    #     :param str amount: transaction amount (up to 15 digits with decimal point)

    #     :return: a dict containing the response code, transaction id and transaction type
    #     :rtype: dict
    #     """
    #     values = {
    #         'createTransactionRequest': {
    #             "merchantAuthentication": {
    #                 "name": self.name,
    #                 "transactionKey": self.cybersource_transaction_key
    #             },
    #             'transactionRequest': {
    #                 'transactionType': 'priorAuthCaptureTransaction',
    #                 'amount': str(amount),
    #                 'refTransId': transaction_id,
    #             }
    #         }
    #     }

    #     response = self._cybersource_request(values)

    #     if response and response.get('err_code'):
    #         return {
    #             'x_response_code': self.AUTH_ERROR_STATUS,
    #             'x_response_reason_text': response.get('err_msg')
    #         }

    #     return {
    #         'x_response_code': response.get('transactionResponse', {}).get('responseCode'),
    #         'x_trans_id': response.get('transactionResponse', {}).get('transId'),
    #         'x_type': 'prior_auth_capture'
    #     }
    
    # # Test
    # def test_authenticate(self):
    #     """Test Authorize.net communication with a simple credentials check.

    #     :return: True if authentication was successful, else False (or throws an error)
    #     :rtype: bool
    #     """
    #     values = {
    #         'authenticateTestRequest': {
    #             "merchantAuthentication": {
    #                 "name": self.name,
    #                 "transactionKey": self.cybersource_transaction_key
    #             },
    #         }
    #     }

    #     response = self._cybersource_request(values)
    #     if response and response.get('err_code'):
    #         return False
    #     return True
