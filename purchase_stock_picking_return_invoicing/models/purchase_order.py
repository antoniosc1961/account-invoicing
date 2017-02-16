# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services
#           <contact@eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.tools.float_utils import float_compare


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('order_line.qty_received',
                 'order_line.move_ids.state',
                 'order_line.move_ids.to_refund_po')
    def _get_invoiced(self):
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        super(PurchaseOrder, self)._get_invoiced()
        for order in self:
            invoice_status = {}
            for line in order.order_line:
                invoice_status[line] = line.order_id.invoice_status
                if line.state == 'purchase' and \
                        line.product_id.purchase_method == 'receive':
                    for move in line.move_ids:
                        if move.state == 'done' \
                                and move.location_id.usage != \
                                'supplier' and move.to_refund_po:
                            qty = move.product_uom._compute_qty_obj(
                                move.product_uom, move.product_uom_qty,
                                line.product_uom)
                            qty_ordered = line.product_qty - qty
                            if float_compare(
                                    line.qty_invoiced, qty_ordered,
                                    precision_digits=precision) == -1:
                                invoice_status[line] = 'to invoice'
                                break
                            else:
                                invoice_status[line] = 'invoiced'
            if any(invoice_status[line] == 'to invoice' for line in
                   invoice_status.keys()):
                order.invoice_status = 'to invoice'
            elif all(invoice_status[line] == 'invoiced' for line in
                     invoice_status.keys()):
                order.invoice_status = 'invoiced'

    @api.multi
    def action_view_invoice_refund(self):
        '''
        This function returns an action that display existing vendor refund
        bills of given purchase order id.
        When only one found, show the vendor bill immediately.
        '''
        action = self.env.ref('account.action_invoice_tree2')
        result = action.read()[0]
        refunds = self.invoice_ids.filtered(lambda x: x.type == 'in_refund')
        # override the context to get rid of the default filtering
        result['context'] = {'type': 'in_refund',
                             'default_purchase_id': self.id}

        if not refunds:
            # Choose a default account journal in the
            # same currency in case a new invoice is created
            journal_domain = [
                ('type', '=', 'purchase'),
                ('company_id', '=', self.company_id.id),
                ('currency_id', '=', self.currency_id.id),
            ]
            default_journal_id = self.env['account.journal'].search(
                journal_domain, limit=1)
            if default_journal_id:
                result['context']['default_journal_id'] = default_journal_id.id
        else:
            # Use the same account journal than a previous invoice
            result['context']['default_journal_id'] = refunds[0].journal_id.id

        # choose the view_mode accordingly
        if len(refunds) != 1:
            result['domain'] = "[('id', 'in', " + \
                               str(refunds.ids) + ")]"
        elif len(refunds) == 1:
            res = self.env.ref('account.invoice_supplier_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = refunds.id
        return result

    @api.depends('order_line.invoice_lines.invoice_id.state')
    def _compute_invoice_refund(self):
        for order in self:
            invoices = self.env['account.invoice']
            for line in order.order_line:
                invoices |= line.invoice_lines.mapped('invoice_id').filtered(
                    lambda x: x.type == 'in_refund')
            order.invoice_refund_count = len(invoices)

    invoice_refund_count = fields.Integer(compute="_compute_invoice_refund",
                                          string='# of Invoice Refunds',
                                          copy=False, default=0)


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends('order_id.state', 'move_ids.state')
    def _compute_qty_received(self):
        super(PurchaseOrderLine, self)._compute_qty_received()
        for line in self:
            bom_delivered = self.sudo()._get_bom_delivered(line.sudo())
            if not bom_delivered:
                for move in line.move_ids:
                    if move.state == 'done' and move.location_id.usage != \
                            'supplier' and move.to_refund_po:
                        qty = move.product_uom._compute_qty_obj(
                            move.product_uom, move.product_uom_qty,
                            line.product_uom)

                        # Multiply the quantity by 2 because in the
                        # original method the quantity is added on a return.
                        # , if the move makes reference to a po line,
                        # which is wrong, because maintaining the reference
                        # to a po line for return moves is very important
                        # for the process of the reconciliation of goods
                        # received not invoiced.
                        line.qty_received -= qty * 2

    @api.depends('invoice_lines.invoice_id.state')
    def _compute_qty_invoiced(self):
        super(PurchaseOrderLine, self)._compute_qty_invoiced()
        for line in self:
            for inv_line in line.invoice_lines:
                if inv_line.invoice_id.state not in ['cancel'] \
                        and inv_line.invoice_id.type == 'in_refund':
                    inv_qty = inv_line.uom_id._compute_qty_obj(
                        inv_line.uom_id, inv_line.quantity, line.product_uom)
                    # Multiply the quantity by 2 because in the
                    # original method the quantity is added when refund
                    # invoices are created with reference to a PO.
                    line.qty_invoiced -= inv_qty * 2
