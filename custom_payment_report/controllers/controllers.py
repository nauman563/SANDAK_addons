# -*- coding: utf-8 -*-
# from odoo import http


# class CustomPaymentReport(http.Controller):
#     @http.route('/custom_payment_report/custom_payment_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_payment_report/custom_payment_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_payment_report.listing', {
#             'root': '/custom_payment_report/custom_payment_report',
#             'objects': http.request.env['custom_payment_report.custom_payment_report'].search([]),
#         })

#     @http.route('/custom_payment_report/custom_payment_report/objects/<model("custom_payment_report.custom_payment_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_payment_report.object', {
#             'object': obj
#         })

