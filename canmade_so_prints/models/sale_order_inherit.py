from pip._internal.utils._jaraco_text import _

from odoo import models, fields, api
from datetime import datetime, timedelta


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    customer_po = fields.Char(string='Customer PO')
    fob = fields.Char(string='FOB')
    shipping_term = fields.Char(string='Shipping Term')
    carrier = fields.Many2one('res.partner', string='Carrier')
    display_price = fields.Float(string='Shipping Amount', readonly=True)
    cancel_date = fields.Datetime(string="Cancel Date", readonly=True)

    def action_cancel(self):
        res = super(SaleOrderInherit, self).action_cancel()
        for order in self:
            order.cancel_date = datetime.now()
        return res

    def _prepare_invoice(self):
        res = super()._prepare_invoice()

        res['customer_po'] = self.customer_po
        return res




    def action_open_delivery_wizard(self):
        view_id = self.env.ref('delivery.choose_delivery_carrier_view_form').id
        if self.env.context.get('carrier_recompute'):
            name = _('Update shipping cost')
            carrier = self.carrier_id
        else:
            name = _('Add a shipping method')
            carrier = (
                    self.with_company(self.company_id).partner_shipping_id.property_delivery_carrier_id
                    or self.with_company(
                self.company_id).partner_shipping_id.commercial_partner_id.property_delivery_carrier_id
            )
        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'choose.delivery.carrier',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_order_id': self.id,
                'default_carrier_id': carrier.id,
                'default_total_weight': self._get_estimated_weight()
            }
        }

    def print_sales_order_report(self):
        # return self.env.ref('canmade_so_print.report_saleorder_document').report_action(self.id)
        return self.env.ref('canmade_so_prints.canmade_sale_order_report_action').report_action(self)



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    shipping_tax = fields.Float(string="Shipping Tax", compute="_compute_shipping_tax_amount", store=True)
    shipping_term = fields.Char(string='Shipping Term')
    carrier = fields.Many2one('res.partner', string='Carrier')
    display_price = fields.Float(string='Shipping Amount', readonly=True)
    shipping_date = fields.Date(string='Shipping Date', readonly=True)

    def _prepare_invoice_line(self, **optional_values):
        """Override to pass journal to created invoice"""
        invoice_vals = super()._prepare_invoice_line()
        invoice_vals['shipping_term'] = self.shipping_term
        invoice_vals['carrier'] = self.carrier.id
        invoice_vals['display_price'] = self.display_price
        invoice_vals['shipping_tax'] = self.shipping_tax
        invoice_vals['shipping_date'] = self.shipping_date

        return invoice_vals

    # locked = fields.Boolean(string="Locked", default=False)

    @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    def _compute_shipping_tax_amount(self):
        for line in self:
            tax_rate = sum(line.tax_id.mapped('amount')) / 100 if line.tax_id else 0.0
            line.shipping_tax = line.product_uom_qty * line.price_unit * tax_rate


class ChooseDeliveryCarrierInherit(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    shipping_term = fields.Char(string='Shipping Term')
    carrier = fields.Many2one('res.partner', string='Carrier')
    display_price = fields.Float(string='Shipping Amount')
    shipping_date = fields.Date(string='Shipping Date')


    def button_confirm(self):
        self.order_id.set_delivery_line(self.carrier_id, self.delivery_price)
        shipping_product = self.order_id.order_line.filtered(lambda rec: rec.product_id.type == 'service')
        if shipping_product:
            shipping_product[0].shipping_term = self.shipping_term
            shipping_product[0].carrier = self.carrier.id
            shipping_product[0].display_price = self.delivery_price
            shipping_product[0].shipping_date = self.shipping_date
        self.order_id.write({
            'recompute_delivery_price': False,
            'delivery_message': self.delivery_message,
        })

# style = "background-color: #d3d3d3;"
