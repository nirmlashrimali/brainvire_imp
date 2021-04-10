from odoo import api, models, fields


class DoctorAppointment(models.Model):
	_name='doctor.appointment'

	name=fields.Char(string='Name')
	age=fields.Integer(string='Age')
	dob=fields.Date(string='Date Of Birth')
	email=fields.Char(string='Email')
	contact=fields.Integer(string='Contact Number')


# class WebAppointment(models.Model):
# 	_inherit='website.page'

# 	name=fields.Char(string='Name')
# 	age=fields.Integer(string='Age')
# 	dob=fields.Date(string='Date Of Birth')
# 	email=fields.Char(string='Email')
# 	contact=fields.Integer(string='Contact Number')
