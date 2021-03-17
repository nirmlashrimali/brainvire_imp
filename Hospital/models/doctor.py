# -*- coding: utf-8 -*-
from odoo import api,models,fields

class Doctor(models.Model):
	_name='doctor.doc'
	_description='creating module for details of doctors'

	name=fields.Char('Name')
	age=fields.Integer('Age')
	email=fields.Char('Email')
	gender=fields.Selection([('male','Male'),('female','Female')],'Gender')
	patient_ids = fields.One2many('patient.pat', 'doctor_id', string="Patients")
	ref=fields.Char('Ref')

	