# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):

        if not args:
            args = []
        if name:
            ids = self.search([(
                'reference', operator, name)], limit=limit)
            ids2 = self.search([('number', operator, name)] + args, limit=limit)
            if ids2:
                ids.extend(ids2)
                ids = list(set(ids))
            if not ids:
                res = super(AccountInvoice, self).name_search(
                                   name=name, args=args, operator=operator, limit=limit)
                if res:
                    ids.update(map(lambda a: a[0], res))


        else:
            ids = self.search(args, limit=limit)
        self.with_context(show_supplier_ref=True)
        result = ids.name_get()
        return result

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            if not self.env.context.get('show_supplier_ref', True):
                return super(AccountInvoice, self).name_get(rec)
            else:
                for val in rec:
                    res.append([val.id, "%s: %s" % (
                        val.number, val.reference)])
            return res
