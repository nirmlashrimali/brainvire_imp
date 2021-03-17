# -*- coding: utf-8 -*-
from odoo import api,models,fields

class ProductBrand(models.Model):
	_name='product.brand'

	name=fields.Char('Brand Name')
	code=fields.Integer('Brand Code')

