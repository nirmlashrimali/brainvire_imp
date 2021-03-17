from odoo import api,models,fields

class EmployeeLib(models.Model):
	_name='employee.lib'
	_description='creating module for details of employee'
	
	name=fields.Char()
	age=fields.Integer('Age')
	email=fields.Char('Email')
	#salary=fields.Float('Salary Of Employee')
	street = fields.Char('Street')
	street2=fields.Char('Street2')
	zip=fields.Char('Zip')
	city=fields.Char('City')
	state_id=fields.Char('State Id')
	country_id=fields.Char('Country Id')

class Department(models.Model):
	_name='department.details'
	_description='creating module for details of department'
	name=fields.Char('Name')
	email=fields.Char("Email")
	details=fields.Text('Details of Department')
   



class Admin(models.Model):
	_name='admin.admin'

	name=fields.Char('Name')
	age=fields.Integer('Age')
	address=fields.Text('Address')
	html=fields.Html('Page')