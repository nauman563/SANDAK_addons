# -*- coding: utf-8 -*-
# from odoo import http


# class CanmadeSoPrint(http.Controller):
#     @http.route('/canmade_so_print/canmade_so_print', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/canmade_so_print/canmade_so_print/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('canmade_so_print.listing', {
#             'root': '/canmade_so_print/canmade_so_print',
#             'objects': http.request.env['canmade_so_print.canmade_so_print'].search([]),
#         })

#     @http.route('/canmade_so_print/canmade_so_print/objects/<model("canmade_so_print.canmade_so_print"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('canmade_so_print.object', {
#             'object': obj
#         })

