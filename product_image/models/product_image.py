# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleProductImage(models.Model):
	_inherit = 'sale.order.line'

	img=fields.Binary(string='Image', related="product_id.image_512")


class StockPickingImage(models.Model):
	_inherit='stock.move'

	img = fields.Binary(string='Image',related="product_id.image_512")


class AccountMoveImage(models.Model):
    _inherit='account.move.line'
  
    img = fields.Binary(string='Image',related="product_id.image_512")


