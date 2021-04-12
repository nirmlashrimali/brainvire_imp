from odoo import api, models, fields


class DoctorAppointment(models.Model):
    _name = 'doctor.appointment'
    _description = 'create appointment for patients'

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age')
    dob = fields.Date(string='Date Of Birth')
    email = fields.Char(string='Email')
    contact = fields.Integer(string='Contact Number')
