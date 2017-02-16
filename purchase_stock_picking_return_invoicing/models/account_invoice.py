# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services
#           <contact@eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def _prepare_invoice_line_from_po_line(self, line):
        data = super(AccountInvoice,
                     self)._prepare_invoice_line_from_po_line(line)
        if line.product_id.purchase_method == 'receive':
            qty = line.qty_received - line.qty_invoiced
            data['quantity'] = qty
        if self.type == 'in_refund':
            data['quantity'] *= -1
        return data
