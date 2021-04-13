# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager


class Appointment(http.Controller):

    @http.route('/appointment', type='http', auth="public", website=True)
    def appointment(self, **kw):
        print("\n\n\n\n\n\n\n-----data sent-----")
        return http.request.render('doctor_appointment.appointment_page_template', {'name': 'nirmla'})

    @http.route('/doctor_appointment_form', type='http', auth="public", website=True)
    def doctor_appointment_form(self, **kw):
        print("-----data received-----")
        request.env['doctor.appointment'].sudo().create(kw)
        return request.render("doctor_appointment.tmp_patients_form_success",{})
  
    @http.route('/my/appointment', type='http', auth="public", website=True)
    def portal_my_appointment(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        partner = request.env.user.partner_id
        WebAppointment = request.env['doctor.appointment'].search([])

        appointment_count = len(WebAppointment)
        searchbar_sortings = {
            'name': {'label': ('Name'), 'appointment': 'name'},
            'age': {'label': ('Age'), 'appointment': 'age'},
        }
              
        if not sortby:
           sortby = 'name'
        sort_appointment = searchbar_sortings[sortby]['appointment']

        pager = portal_pager(
        url="/my/appointment",

        total=appointment_count,
        page=page
        )
        # search the count to display, according to the pager data
        appointment = WebAppointment
        print("----__________---------________\n\n\n\n",appointment)
        request.session['my_appointment_history'] = appointment.ids[:100]

        values={
        'appointments': appointment.sudo(),
        'page_name': 'Appointment',
        'pager': pager,
        'default_url': '/my/appointment',

        }
        print("--------------------------\n\n\n\n\n\n\n",values)
        return request.render("doctor_appointment.portal_my_appointments", values)

