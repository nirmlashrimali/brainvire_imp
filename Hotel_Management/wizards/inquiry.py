# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError, ValidationError


class HotelInquiry(models.TransientModel):
    _name='hotel.inquiry'
    _description='Inquiry about Hotel and Rooms Avaibility'

    customer=fields.Many2one('res.partner','Customer')
    start_date=fields.Date('Start Date')
    end_date=fields.Date('End Date')
    room_types=fields.Many2one('room.type','Room Type')
    room_size_id=fields.Integer('Room Size')

    def search_room_available(self):
        # check_room=self.env['hotel.room'].search([('room_type_id','=',self.room_types.id),('room_size','>=',self.room_size_id)])
        # print("\n\n\ncheck_room--->",check_room)
        get_record=self.env['hotel.room'].search([('date_from','>=',self.start_date),('date_to','<=',self.end_date),('room_type_id','=',self.room_types.id),('room_size','>=',self.room_size_id)])
        print("get_record-->",get_record)
        if get_record:
            return {
                    'res_model':'hotel.registration',
                    'type': 'ir.actions.act_window',
                    'context': {},
                    'view_mode': 'form',
                    'view_type': 'form',
                    'view_id': self.env.ref("Hotel_Management.registration_form_view").id,
                    'target': 'new'
                }
        else:
            raise ValidationError(_('No room Available'))
            print("__________----------________________-------------________________----------_______________--")


# class RoomInquiry(models.TransientModel):
#     _name='room.inquiry'

#     register_ids=fields.Many2many('hotel.registration','Registrations')