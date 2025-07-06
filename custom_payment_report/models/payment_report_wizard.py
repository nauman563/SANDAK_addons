from odoo import api, fields, models

class PaymentReportWizard(models.TransientModel):
    _name = 'payment.deduction.report.wizard'
    _description = 'Payment Report Wizard'

    journal_ids = fields.Many2many('account.journal', string="Banks", domain=[('type', '=', 'bank')])
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    def generate_pdf_report(self):
        data = {
            'journal_ids': self.journal_ids.ids,
            'from_date': self.from_date,
            'to_date': self.to_date,
        }
        return self.env.ref('custom_payment_report.employee_deduction_action_id').report_action(self, data=data)

class PaymentReport(models.AbstractModel):
    _name = 'report.custom_payment_report.report_payment_of_deductions'
    _description = 'Payment Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        journal_ids = data.get('journal_ids')
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        formatted_date = 'CURRENT MONTH'
        if from_date:
            try:
                if isinstance(from_date, str):
                    from_date = fields.Date.from_string(from_date)
                formatted_date = from_date.strftime('%B-%Y').upper()
            except Exception:
                formatted_date = 'CURRENT MONTH'

        domain = [('date', '>=', from_date), ('date', '<=', to_date)]
        if journal_ids:
            domain.append(('journal_id', 'in', journal_ids))

        payments = self.env['account.payment'].search(domain)

        all_tax_names = set()
        for payment in payments:
            for invoice in payment.reconciled_bill_ids:
                for line in invoice.invoice_line_ids:
                    for tax in line.tax_ids:
                        all_tax_names.add(tax.name)
        all_tax_names = sorted(all_tax_names)

        payment_taxes = {}
        for payment in payments:
            taxes_dict = {tax_name: 0.0 for tax_name in all_tax_names}
            for invoice in payment.reconciled_bill_ids:
                for line in invoice.invoice_line_ids:
                    for tax in line.tax_ids:
                        if tax.name in taxes_dict:
                            taxes_dict[tax.name] += line.price_total * tax.amount / 100
            payment_taxes[payment.id] = taxes_dict

        return {
            'doc_ids': docids,
            'doc_model': 'account.payment',
            'docs': payments,
            'from_date': from_date,
            'to_date': to_date,
            'formatted_date': formatted_date,
            'journals': self.env['account.journal'].browse(journal_ids) if journal_ids else None,
            'all_tax_names': all_tax_names,
            'payment_taxes': payment_taxes,
        } 