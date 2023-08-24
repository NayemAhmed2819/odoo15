# -*- coding: utf-8 -*-
# from odoo import http


# class OdooInheritence(http.Controller):
#     @http.route('/odoo_inheritence/odoo_inheritence', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_inheritence/odoo_inheritence/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_inheritence.listing', {
#             'root': '/odoo_inheritence/odoo_inheritence',
#             'objects': http.request.env['odoo_inheritence.odoo_inheritence'].search([]),
#         })

#     @http.route('/odoo_inheritence/odoo_inheritence/objects/<model("odoo_inheritence.odoo_inheritence"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_inheritence.object', {
#             'object': obj
#         })
