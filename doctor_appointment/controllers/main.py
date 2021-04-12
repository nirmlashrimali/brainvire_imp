# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


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
