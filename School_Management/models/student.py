from odoo import api,models,fields
from datetime import datetime,date
import datetime
from dateutil.relativedelta import relativedelta



class StudentMaster(models.Model):
    _name="student.master"
    _description='creating module for details of students'

    name=fields.Char(string='Name',required=True)
    dob=fields.Date(string='Date Of Birth')
    email=fields.Char(string='Email',required=False)
    age=fields.Char(string='Age')
    gender=fields.Selection([('male','Male'),('female','Female')],'Gender')
    image=fields.Binary("Pic")

    @api.onchange('dob')
    def onchange_dob(self):
        if self.dob:
            years = relativedelta(date.today(), self.dob).years
            self.age = str(int(years))
           # months = relativedelta(date.today(), self.dob).months
            #day = relativedelta(date.today(), self.dob).days
            # self.age = str(int(years)) + ' Year/s ' + str(int(months)) + ' Month/s ' + str(day) + ' Day/s'
    


    def search_name(self):
        print("self----->",self)

        active_model=self.env.context.get('active_model')
        print("active model---->",active_model)
        name=self.env['student.master'].browse(self.env.context.get('active_ids'))
        print(self.env.ref('student.master'))
        print("name----->",self.name)
        print(self.create({'name':'pari'}))
        
    ''' print(self.search([('name','=','prince')]))
        print(self.write({'name':'maahi'}))
        print(self.browse([7,8,12]))
        print(self.search_read([], ['name']))'''
