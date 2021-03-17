from odoo import api,models,fields
from lxml import etree

class SaleOrder(models.Model):
	_inherit='sale.order'

	#name=fields.Char('Product')
	brand_sale_id=fields.Many2one('product.brand',string='Brand')

	
	@api.model 
	def _fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
		res = super(SaleOrder, self)._fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
		doc = etree.XML(res['arch']) 
		for node in doc.xpath("//field[@name='brand_sale_id']"):
			node.set('required','True')
		res['arch']=etree.tostring(doc)
		return res






class SaleOrderline(models.Model):
	_inherit='sale.order.line'
	_description='extend sale order'


class ResPartner(models.Model):
	_inherit='res.partner'

	
	def name_get(self):
			res = []
			for record in self:
				res.append((record.id, '%s %s' % (record.name,record.phone)))
			return res

   


''' def name_get(self):
			res = []
			for record in self:
				res.append((record.id, '%s %s' % (record.name,record.phone)))
			return res'''

	

