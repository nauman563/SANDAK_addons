from odoo import api, fields, models


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    customer_po = fields.Char(string='Customer PO', readonly=True)

    def print_invoice_report(self):
        # return self.env.ref('canmade_so_print.report_saleorder_document').report_action(self.id)
        return self.env.ref('canmade_so_prints.canmade_invoice_report_action').report_action(self)

class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    shipping_term = fields.Char(string='Shipping Term')
    carrier = fields.Many2one('res.partner', string='Carrier')
    display_price = fields.Float(string='Shipping Amount', readonly=True)
    shipping_tax = fields.Float(string="Shipping Tax",)
    shipping_date = fields.Date(string='Shipping Date')

