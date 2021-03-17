# -*- coding: utf-8 -*-
from odoo import api,models,fields
from odoo.osv import expression

class StudentStud(models.Model):
    _name='student.stud'
    _rec_name='std_id'

    name=fields.Char('Name')
    sequence=fields.Char('Sequence', readonly=True, required=True, index=True, default='New')
    dob=fields.Date('Date Of Birth')
    # std=fields.Integer('Std')
    email=fields.Char('Email')
    gender=fields.Selection([('male','Male'),('female','Female')],'Gender')
    pic=fields.Binary('Pic')
    teacher_id=fields.Many2one('teacher.recruit','Teacher')
    std_id=fields.Many2one('standard.std','Std')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('process', 'Process'),
            ('done','Done')
            ],default='draft')

    def done_progressbar(self):
       for rec in self: 
        rec.state = 'done'

    def process_progressbar(self):
       for rec in self: 
        rec.state = 'process'

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('student.stud') or 'New'
        result = super(StudentStud, self).create(vals)
        return result
    

        

class TeacherRecruitment(models.Model):
    _name='teacher.recruit'

    name=fields.Char('Name')
    sequence=fields.Char('Sequence',readonly=True, required=True, index=True, default='New')
    age=fields.Integer('Age')
    exp=fields.Integer('Experience')
    sub=fields.Char('Subject')
    #std=fields.Integer('Std')
    email=fields.Char('Email')
    gender=fields.Selection([('male','Male'),('female','Female')],'Gender')
    doc_ids=fields.One2many('document.doc','teacher_id','Documents',)
    join_date=fields.Date('Joining Date')
    student_ids=fields.One2many('student.stud','teacher_id',string="Students",domain="[('state', '=', 'done')]")
    current = fields.Boolean(string = "Active", required = True)
    marital=fields.Selection([('single','Single'),('married','Married')],string='Marital')
    spouse_complete_name=fields.Char('Spouse Name')
    spouse_birthdate=fields.Date('Spouse Birth Date')
    certificate=fields.Selection([('graduate','Graduate'),('bachelor','Bachelor'),('master','Master'),('doctor','Doctor')],'Certificate')
    study_field=fields.Char('Study Level')
    study_school=fields.Char('Study School')
    std_ids=fields.Many2many('standard.std',string='Standards')
    state=fields.Selection([
            ('draft', 'Draft'),
            ('process', 'Process'),
            ('demo','Demo'),
            ('done','Done')

            ],default='draft')

    def done_progressbar(self):
       for rec in self: 
        rec.state = 'done'

    def process_progressbar(self):
       for rec in self: 
        rec.state = 'process'

    def demo_progressbar(self):
       for rec in self: 
        rec.state = 'demo'

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('teacher.recruit') or 'New'
        result = super(TeacherRecruitment, self).create(vals)
        return result
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        
        context=self._context
        print("Context--111111->",self._context)
        if args is None:
            args = []
        else:
            if context.get('std'):
                standard_ids = self.env['standard.std']._search([('id',operator,context.get('std'))],limit=limit)
                print("standard_ids--->",standard_ids)
                domain = [('std_ids','=',standard_ids)]
                
            else:
                print("kmkjnhjbh")  
                domain = []
        return self._search(expression.AND([domain,args]),limit=limit)

   
        

    


class Document(models.Model):
    _name='document.doc'

    name=fields.Char('Name')
    date=fields.Date('Date')
    doc=fields.Binary('Document',required=True)
    teacher_id=fields.Many2one('teacher.recruit','Teacher')


class StandardStd(models.Model):
    _name='standard.std'
    _rec_name='std'

    std=fields.Integer('Std')


    
   