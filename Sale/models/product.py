from odoo import api,models,fields
from odoo.osv import expression

class ProductProduct(models.Model):
	_inherit='product.product'

	brand_id=fields.Many2one('product.brand',string='Brand')


	@api.model
	def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
		context=self.env.context
		#print("context--->",context)
	   
		if context.get('br_id'):
			print("context-->",context)
			domain=[('brand_id','=',context.get('br_id'))]
			return self._search(expression.AND([domain,args]),limit=limit)
		else:return self._search(expression.AND([domain,args]),limit=limit)