# coding: utf-8
from odoo import api, models, fields
from werkzeug import urls
import logging
_logger = logging.getLogger(__name__)


class PaymentCyberSource(models.Model):
    _inherit = 'payment.acquirer'

    provider =fields.Selection(selection_add=[
        ('cybersource', 'CyberSource')], ondelete={'cybersource': 'set default'})
    authorize_login = fields.Char(string='API Login Id', required_if_provider='authorize', groups='base.group_user')
    authorize_transaction_key = fields.Char(string='API Transaction Key', required_if_provider='authorize', groups='base.group_user')
   