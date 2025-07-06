from odoo import api, fields, models ,api


class SaleOrderInherit(models.Model):
    _inherit = 'purchase.order'


    customer_po = fields.Char(string='Customer PO',tracking=True)
    shipping_method = fields.Many2one('delivery.carrier',
                                      string="Shipping Method",
                                      tracking=True)
    shipping_term = fields.Char(string="Shipping Term", tracking=True)
    shipping = fields.Char(string="Shipping.#", tracking=True)
    carrier = fields.Char(string="Carrier" ,tracking=True)
    vendor_msg = fields.Text(string="Vendor Msg", tracking=True)
    fob = fields.Char('FOB', tracking=True)

    def print_purchase_order_report(self):
        # return self.env.ref('canmade_so_print.report_saleorder_document').report_action(self.id)
        return self.env.ref('canmade_so_prints.canmade_purchase_order_report_action').report_action(self)

    def purchase_order_report(self):
        # return self.env.ref('canmade_so_print.report_saleorder_document').report_action(self.id)
        return self.env.ref('canmade_so_prints.canmade_purchase_order_action').report_action(self)

