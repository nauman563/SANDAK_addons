# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class custom_payment_report(models.Model):
#     _name = 'custom_payment_report.custom_payment_report'
#     _description = 'custom_payment_report.custom_payment_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

