# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openerp import _, api, fields, models
from openerp.exceptions import UserError


class WizardModel(models.TransientModel):
    _name = "purchase.batch_invoicing"

    purchase_order_ids = fields.Many2many(
        comodel_name="purchase.order",
        string="Purchase orders",
        domain="[('invoice_status', '=', 'to invoice')]",
        required=True,
        readonly=True,
        default=lambda self: self._default_purchase_order_ids(),
    )
    grouping = fields.Selection(
        selection=[
            ("id", "Purchase Order"),
            ("partner_id", "Vendor"),
        ],
        required=True,
        default="id",
        help="Make one invoice for each...",
    )

    @api.model
    def _default_purchase_order_ids(self):
        """Get purchase orders from active ids."""
        try:
            return self.env["purchase.order"].search(
                self._purchase_order_domain(self.env.context["active_ids"])
            ).ids
        except KeyError:
            return False

    @api.model
    def _purchase_order_domain(self, ids):
        """Helper to filter current ids by those that are to invoice."""
        return [
            ("id", "in", ids),
            ("invoice_status", "=", "to invoice"),
        ]

    @api.multi
    def grouped_purchase_orders(self):
        """Purchase orders, applying current grouping.

        :return generator:
            Generator of grouped ``purchase.order`` recordsets.

            If :attr:`grouping` is ``id``, the generator will yield recordsets
            with 1 order each; if it is ``partner_id``, the yielded recordsets
            will contain all purchase orders from each vendor.
        """
        PurchaseOrder = self.env["purchase.order"]
        domain = self._purchase_order_domain(self.purchase_order_ids.ids)
        for group in self.mapped("purchase_order_ids.%s" % self.grouping):
            pos = PurchaseOrder.search(
                domain + [(self.grouping, "=", int(group))])
            pos = pos.filtered(lambda order: (
                sum(order.mapped("order_line.qty_invoiced")) <
                sum(order.mapped("order_line.qty_received"))))
            if pos:
                yield pos

    @api.multi
    def action_batch_invoice(self):
        """Generate invoices for all selected purchase orders.

        :return dict:
            Window action to see the generated invoices.
        """
        invoices = self.env["account.invoice"]
        for pogroup in self.grouped_purchase_orders():
            # HACK https://github.com/odoo/odoo/pull/13082
            with invoices.env.do_in_onchange():
                invoice = invoices.new({
                    "partner_id": pogroup.mapped("partner_id").id,
                    "type": "in_invoice",
                })
                invoice._onchange_partner_id()
                for po in pogroup:
                    invoice.currency_id = po.currency_id
                    invoice.purchase_id = po
                    invoice.purchase_order_change()
                vals = invoice._convert_to_write(invoice._cache)
            invoices |= invoices.create(vals)
        if not invoices:
            raise UserError(_("No ready to invoice purchase orders selected."))
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.invoice",
            "name": _("Generated Invoices"),
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", invoices.ids]],
        }
