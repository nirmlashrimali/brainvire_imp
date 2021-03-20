# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import date, timedelta


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _rec_name = 'room_type_id'
    _rec_name = 'room_no'

    room_no = fields.Char('Room Number', readonly=True, required=True, index=True, default='New')
    room_type_id = fields.Many2one('room.type', string='Room Type Id')
    floor = fields.Selection([('one', '1'), ('two', '2'), ('three', '3')], string='Floor')
    room_size = fields.Integer('Room Size')
    # date_from=fields.Date('Start Date')
    # date_to=fields.Date('End Date')
    inquiry_id = fields.Many2one('hotel.inquiry', 'Inquiry')
    book_room = fields.Boolean('Room Book')
    price = fields.Integer('Price')
    room_state = fields.Selection([
        ('draft', 'Draft'),
        ('allocated', 'Allocated')
    ], default='draft')

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
    _name = 'hotel.registration'
    _rec_name = 'name'

    # name=fields.Many2one('res.partner')
    name = fields.Char('Name')

    register_no = fields.Char('Regsiter Number', readonly=True, required=True, index=True, default='New')
    phone = fields.Integer('Contact Number')
    dob = fields.Date('Birth Date')
    # email=fields.Char('Email')
    doc_ids = fields.One2many('register.document', 'registration_id', string='Documents', required=True)
    # room_id=fields.Many2one('hotel.room','Rooms')
    date_from = fields.Date('Start Date')
    date_to = fields.Date('End Date')
    total  = fields.Float('Total',readonly=1)
    # create_date=fields.Date(default=date.today())
    state = fields.Selection([
        ('draft', 'Draft'),
        ('process', 'Process'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], default='draft')
    # line_ids=fields.One2many('room.guest.line.','reg_id',string='Room Customer Guests')
    line_ids = fields.One2many('room.guest.line', 'reg_id', string='Room Customer Guest')

    def done_progressbar(self):
        for rec in self:
            rec.state = 'done'
            rec.line_ids.room_id.room_state = 'allocated'

    def process_progressbar(self):
        for rec in self:
            rec.state = 'process'

    def cancel_progressbar(self):
        for rec in self:
            rec.state = 'cancel'

    def action_registration_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']

        try:
            template_id = self.env['ir.model.data'].xmlid_to_res_id('hotel_management.email_template_reg',
                                                                    raise_if_not_found=False)
            print(template_id, "template_id\n\n\n\n\n")
        except ValueError:
            print("\n\n\n\n value error \n\n\n\n\n\n")
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False

        ctx = {
            'default_model': 'hotel.registration',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        }
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.model
    def create(self, vals):
        if vals.get('register_no', 'New') == 'New':
            vals['register_no'] = self.env['ir.sequence'].next_by_code('hotel.registration') or 'New'
        result = super(HotelRegistration, self).create(vals)
        return result

    @api.model
    def _registration_cancel(self):
        print("--\n\n\n--->", self)
        var = self.env['hotel.registration'].search([('state', '!=', 'done')])
        for i in var:
            if ((date.today()) - (i.create_date)) > timedelta(days=3):
                i.state = 'cancel'

                print("\n\n\n\n\n\n\n\n--")
                print("\n\n\n\n\n\n\n\n--")
            else:
                print("\n\n\n\n\n\n\n\n--")


    
class RegisterDocument(models.Model):
    _name = 'register.document'

    name = fields.Char('Name')
    date = fields.Date('Date')
    doc = fields.Binary('Document', required=True)
    registration_id = fields.Many2one('hotel.registration', string='Registration Id')


# class CustomerGuest(models.Model):
#     _name = 'customer.guest'

#     name = fields.Char('Guest Name')
#     age = fields.Integer('Guest Age')
#     # register_id=fields.Many2one('hotel.registration','Register Id')


class RoomType(models.Model):
    _name = 'room.type'
    _rec_name = 'room_type'

    room_type = fields.Char('Room Type')


class HotelInquiry(models.Model):
    _name = 'hotel.inquiry'
    _description = 'Inquiry about Hotel and Rooms Avaibility'
    _rec_name = 'customer'

    customer = fields.Many2one('res.partner', string='Customer', required=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    room_types = fields.Many2one('room.type', 'Room Type')
    room_size_id = fields.Integer('Room Size')
    room_ids = fields.One2many('hotel.room', 'inquiry_id', string='Room')
    total_price=fields.Integer('Total Price',compute='compute_price')

    
    @api.onchange('room_ids')
    def compute_price(self):
         total=0
         for record in self.room_ids:
            if  record.book_room:
                total+=record.price
         self.write({
            'total_price':total
            })
            


    def search_room_available(self):
        check_room = self.env['hotel.room'].search(
            [('room_state', '=', 'draft'), ('room_type_id', '=', self.room_types.id),
             ('room_size', '>=', self.room_size_id)])
        print("\n\n\n\n\n---->", check_room)
        if check_room:
            self.room_ids = [(6, 0, [])]
            print("-----t-->", self.room_ids)
            self.write({'room_ids': check_room})
            return


        else:
            raise ValidationError(_('No room Available'))
            print("__________----------________________-------------________________----------_______________--")

    def get_record(self):
        records = self.env['hotel.inquiry'].browse('active_ids')
        print("---------->", records)

        res = []
        for i in self:
            for j in i.room_ids:
                if j.book_room:
                    res.append({'room_id': j.id})
                    print("----------->", res)

        contexts = {
            # 'default_room_id':rooms,
            'default_line_ids': res,
            'default_name': self.customer.name,
            'default_date_from': self.start_date,
            'default_date_to': self.end_date,
            'default_total':self.total_price
        }
        
        if records:
            return {
                'res_model': 'hotel.registration',
                'type': 'ir.actions.act_window',
                'context': contexts,
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': self.env.ref("hotel_management.registration_form_view").id,
                'target': 'new'
            }


class RoomGuestLine(models.Model):
    _name = 'room.guest.line'
    _description = 'Inquiry about customer and their guests Avaibility'
    _rec_name = 'room_id'

    room_id = fields.Many2one("hotel.room", 'Room')
    guest_ids = fields.Many2many('res.partner', string='Guests')
    reg_id = fields.Many2one('hotel.registration', 'Register Id')




class Registration(models.AbstractModel):
    _name = 'report.hotel_management.report_registration'
    _description = 'get values data'

    def _get_method(self, doc):
        print("---\\n\n\n\n\n---")
        return "5"

    @api.model
    def _get_report_values(self, docids, data=None):
        print("\n\n\n\n\n\n\n\n\n re")
        docs = self.env['hotel.registration'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'hotel.registration',
            'docs': docs,
            'data': data,
            'get_method': self._get_method,
        }
