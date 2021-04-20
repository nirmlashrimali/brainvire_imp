# coding: utf-8
from odoo import api, models, fields
from werkzeug import urls
import logging
_logger = logging.getLogger(__name__)


class PaymentCyberSource(models.Model):
    _inherit = 'payment.acquirer'

    provider =fields.Selection(selection_add=[
        ('cybersource', 'CyberSource')], ondelete={'cybersource': 'set default'})
    cybersource_login = fields.Char(string='API Login Id', required_if_provider='cybersource', groups='base.group_user')
    cybersource_transaction_key = fields.Char(string='API Transaction Key', required_if_provider='cybersource', groups='base.group_user')
   
    def _get_feature_support(self):
        """Get advanced feature support by provider.
        Each provider should add its technical in the corresponding
        key for the following features:
            * fees: support payment fees computations
            * authorize: support authorizing payment (separates
                         authorization and capture)
            * tokenize: support saving payment data in a payment.tokenize
                        object
        """
        res = super(PaymentCyberSource, self)._get_feature_support()
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
        # State code is only supported in US, use state name by default
        state = values['partner_state'].name if values.get('partner_state') else ''
        if values.get('partner_country') and values.get('partner_country') == self.env.ref('base.us', False):
            state = values['partner_state'].code if values.get('partner_state') else ''
        billing_state = values['billing_partner_state'].name if values.get('billing_partner_state') else ''
        if values.get('billing_partner_country') and values.get('billing_partner_country') == self.env.ref('base.us', False):
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
        print("\n\n\n\n\n\ncybersource_get_form_action------\n\n\n\n\n\n")
        self.ensure_one()
        environment = 'prod' if self.state == 'enabled' else 'test'
        return self._get_cybersource_urls(environment)['cybersource_form_url']


    # @api.model
    # def cybersource_s2s_form_process(self, data):
    #     print("\n\n\n\n\n\ncybersource_s2s_form_process------\n\n\n\n\n\n")

    #     values = {
    #         'opaqueData': data.get('opaqueData'),
    #         'encryptedCardData': data.get('encryptedCardData'),
    #         'acquirer_id': int(data.get('acquirer_id')),
    #         'partner_id': int(data.get('partner_id'))
    #     }
    #     PaymentMethod = self.env['payment.token'].sudo().create(values)
    #     return PaymentMethod


    def cybersource_test_credentials(self):
        print("\n\n\n\n\n\ncybersource_test_credentials-----\n\n\n\n\n\n")
        self.ensure_one()
        transaction = CyberSourceAPI(self.acquirer_id)
        return transaction.test_authenticate()

# class PaymentToken(models.Model):
#     _inherit = 'payment.token'

#     cybersource_profile = fields.Char(string='CyberSource Profile ID', help='This contains the unique reference '
#                                     'for this partner/payment token combination in the CyberSource backend')
#     provider = fields.Selection(string='Provider', related='acquirer_id.provider', readonly=False)
#     save_token = fields.Selection(string='Save Cards', related='acquirer_id.save_token', readonly=False)
