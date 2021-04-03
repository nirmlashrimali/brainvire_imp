# -*- coding: utf-8 -*-
from odoo import api, models, fields,_
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrderExtend(models.Model):
    _inherit='sale.order'

    discount_type=fields.Selection([('amount','Amount'),('percentage','Percentage')],string='Discount Type')
    global_discount=fields.Float(string='Global Discount')

    
    
    #     else (self.discount_type == self.percentage) and (self.global_discount<1 or self.global_discount>100):
    #            raise ValidationError(_('Amount is more then total amount'))
    #            print("__________----------________________-------------________________----------_______________--")
    
    @api.constrains('global_discount')   
    def get_amount(self): 

        # res = super(SaleOrder, self).amount_total()
        if self.discount_type == 'amount' and self.global_discount > self.amount_total:
                raise ValidationError(_('amount should not exceed amount total'))
                print("__________----------________________-------------________________----------_______________--")
        
        elif (self.discount_type == 'percentage') and (self.global_discount<1 or self.global_discount>100):
                raise ValidationError(_('percentage is bitween 1-100'))
                print("__________----------________________-------------________________----------_______________--")

    @api.depends('global_discount', 'discount_type')   
    def _amount_all(self):
        res = super(SaleOrderExtend, self)._amount_all()

        if self.discount_type == 'amount':
            self.amount_total=self.amount_total-self.global_discount

        elif self.discount_type == 'percentage':
            percent=self.amount_total* self.global_discount/100
            self.amount_total=self.amount_total-percent
        return res

        
    