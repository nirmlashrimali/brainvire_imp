# -*- coding: utf-8 -*-
from odoo import api,models,fields

class  CrmLead(models.Model):
	_inherit='sale.order'

	new_field=fields.Char('Name')
	expiry=fields.Date('Expiry')
	age=fields.Char('Age')
	#name=fields.Char('Name')