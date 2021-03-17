# -*- coding: utf-8 -*-
from odoo import api,models,fields,_
from odoo.exceptions import AccessError, UserError, ValidationError

class Patient(models.Model):
	_name='patient.pat'
	_description='creating module for details of patients'

	name=fields.Char('Name')
	age=fields.Integer('Age')
	email=fields.Char('Email')
	gender=fields.Selection([('male','Male'),('female','Female')],'Gender')
	issue_date=fields.Date('Issue Date')
	notes=fields.Text('Notes')
	state = fields.Selection([
			('draft', 'Draft'),
			('done', 'Done')
			],default='draft')
	doctor_id=fields.Many2one('doctor.doc',string='Doctor')
	line_ids=fields.One2many('patient.line','patient_id','Lines')
	doc_ids=fields.Many2many('doctor.doc',string='Doctors')
	grand_total=fields.Integer('Grand Total' ,compute='compute_grand_total')


	

	def done_progressbar(self):
	   for rec in self: 
	   	rec.state = 'done'
	   	for tab in rec.line_ids:
		   	tab.tablet_id.quantity = tab.tablet_id.quantity-tab.qty

	@api.depends('line_ids.total')
	def compute_grand_total(self):
		t=0
		for record in self:
			for rec in record.line_ids:
				t+=rec.total
			record.grand_total=t


class Tablet(models.Model):
	_name='patient.tablet'

	name=fields.Char('Tablet Name')
	quantity=fields.Integer('Quantity')

	@api.constrains('quantity')
	def _check_quantity(self):
		if self.quantity < 0:
			raise ValidationError(_('stock is out of order.'))
	
class Line(models.Model):
	_name='patient.line'

	tablet_id=fields.Many2one('patient.tablet','Tablet')
	patient_id=fields.Many2one('patient.pat','Patient')
	qty=fields.Integer('Qty')
	price=fields.Integer("price")
	total=fields.Integer("Total")



	@api.onchange('price','qty')
	def onchange_total(self):
		for record in self:
			record.total=(record.price*record.qty)

	