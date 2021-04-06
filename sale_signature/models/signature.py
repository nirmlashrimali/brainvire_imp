# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrderSignature(models.Model):
    _inherit = 'sale.order'

    sign=fields.Text(string='Signature')

    def action_view_delivery(self):
        res = super(SaleOrderSignature, self).action_view_delivery()
        self.picking_ids.write({'sign': self.sign})
        return res
    
    def action_view_invoice(self):
        res = super(SaleOrderSignature, self).action_view_invoice()
        self.invoice_ids.write({'sign': self.sign})
        return res
    

   
class StockPicking(models.Model):
    _inherit='stock.picking'

    sign=fields.Text(string='Signature')

    

class AccountMove(models.Model):
    _inherit='account.move'

    sign=fields.Text(string='Signature')

      