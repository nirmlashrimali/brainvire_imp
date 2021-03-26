# -*- coding: utf-8 -*-
from odoo import api, models, fields

class ResConfigSettings(models.TransientModel):
	_inherit='res.config.settings'

	sale_limit=fields.Float(string='Sale Limit')