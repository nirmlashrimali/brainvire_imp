# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HotelRoom(models.Model):
    _name='hotel.room'
    _rec_name='room_type_id'
    

    room_no=fields.Char('Room Number',readonly=True, required=True, index=True, default='New')
    room_type_id=fields.Many2one('room.type',string='Room Type Id')
    floor=fields.Selection([('one','1'),('two','2'),('three','3')],string='Floor')
    room_size=fields.Integer('Room Size')
    date_from=fields.Date('Start Date')
    date_to=fields.Date('End Date')
    room_state = fields.Selection([
            ('draft', 'Draft'),
            ('allocated', 'Allocated')
            ],default='draft')

    def allocated_progressbar(self):
       for rec in self: 
        rec.room_state = 'allocated'

    @api.model
    def create(self, vals):
        if vals.get('room_no', 'New') == 'New':
            vals['room_no'] = self.env['ir.sequence'].next_by_code('hotel.room') or 'New'
        result = super(HotelRoom, self).create(vals)
        return result


class HotelRegistration(models.Model):
    _name='hotel.registration'

    name=fields.Char('Customer Name')
    register_no=fields.Char('Regsiter Number',readonly=True, required=True, index=True, default='New')
    phone=fields.Integer('Contact Number')
    dob=fields.Date('Birth Date')
    doc_ids=fields.One2many('register.document','registration_id',string='Documents',required=True)
    state = fields.Selection([
            ('draft', 'Draft'),
            ('process','Process'),
            ('done','Done')
            ],default='draft')
    guest_ids=fields.One2many('customer.guest','register_id',string='Guests')
    room_id=fields.Many2one('hotel.room',string='Room',domain=[('room_state', '=', 'draft')])

    def done_progressbar(self):
       for rec in self: 
        rec.state = 'done'

    def process_progressbar(self):
       for rec in self: 
        rec.state = 'process'


    @api.model
    def create(self, vals):
        if vals.get('register_no', 'New') == 'New':
            vals['register_no'] = self.env['ir.sequence'].next_by_code('hotel.registration') or 'New'
       

        val={'room_state':'allocated'}
        room_allocate = self.env['hotel.room'].search([('id', '=', vals['room_id'])])
        for i in room_allocate:
                i.write(val)

        result = super(HotelRegistration, self).create(vals)
        return result


class RegisterDocument(models.Model):
    _name='register.document'

    name=fields.Char('Name')
    date=fields.Date('Date')
    doc=fields.Binary('Document',required=True)
    registration_id=fields.Many2one('hotel.registration',string='Registration Id')


class CustomerGuest(models.Model):
    _name='customer.guest'

    name=fields.Char('Guest Name')
    age=fields.Integer('Guest Age')
    register_id=fields.Many2one('hotel.registration','Register Id')


class RoomType(models.Model):
    _name='room.type'
    _rec_name='room_type'

    room_type=fields.Char('Room Type')