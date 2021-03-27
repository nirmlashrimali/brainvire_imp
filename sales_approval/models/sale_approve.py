# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResConfigSettings(models.TransientModel):
    _inherit='res.config.settings'

    sale_limit=fields.Float(string='Sale Limit', config_parameter="sales_approval.sale_limit")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        res['sale_limit'] = (self.env['ir.config_parameter'].sudo().get_param('sales_approval.sale_limit',
        default=0))
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('sales_approval.sale_limit', self.sale_limit)
        super(ResConfigSettings, self).set_values()


class SaleOrder(models.Model):
    _inherit='sale.order'

    state = fields.Selection(selection_add=([('to_approve','To Approve')]))

    def get_approve(self):
    	self.state='sale'

    def action_confirm(self):
        res = super(SaleOrder ,self).action_confirm()
        sales_limit = self.env['ir.config_parameter'].sudo().get_param('sales_approval.sale_limit') or False
        print("---\n\n\n\\--->",sales_limit)
        if sales_limit:
            if float(self.amount_total) > float(sales_limit):
            	self.state = 'to_approve'
        return res