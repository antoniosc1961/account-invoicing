# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services
#           <contact@eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def _prepare_invoice_line_from_po_line(self, line):
        data = super(AccountInvoice,
                     self)._prepare_invoice_line_from_po_line(line)
        if line.product_id.purchase_method == 'receive':
            qty = line.qty_received - line.qty_invoiced
            data['quantity'] = qty
        if self.type == 'in_refund':
            invoice_line = self.env['account.invoice.line']
            data['quantity'] *= -1
            data['account_id'] = invoice_line.with_context(
                {'journal_id': self.journal_id.id,
                 'type': 'in_refund'})._default_account(),
        return data
