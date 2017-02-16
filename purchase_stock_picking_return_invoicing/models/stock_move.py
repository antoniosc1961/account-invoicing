# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services
#           <contact@eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    to_refund_po = fields.Boolean(
        "To Refund in PO",
        help='Trigger a decrease of the received quantity in the associated '
             'Purchase Order',
    )
