.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================
Refund Returned Pickings from Purchase Orders
=============================================

This module extends the functionality of purchase orders to support marking some
returned pickings as "To refund in Purchase Order",  excluding those quantities
from the quantity to invoice, when the product is to be invoiced based on
received quantities.

Usage
=====

Case 1: When you return to a supplier some products, and you have not yet
received the bill from the supplier

#. Go to *Purchases > Purchase > Purchase Orders > Create*.
#. Choose a supplier and add a product whose *Invoicing Policy* is *On Received
   quantities*, and input some quantity to purchase.
#. Confirm the purchase order.
#. Go to *Shipment > Validate > Apply* so as to receive the quantities ordered.
#. Press the button *Reverse*.
#. In the wizard *Reverse Quantity* Set *Quantity* to the quantity to be
   returned. Press *Return* to complete the wizard.
#. On the return picking press *Validate > Apply*.
#. Go back to the purchase order. You will notice that the field *Received
   Qty* is now the quantity that was originally received, less the quantity
   that was returned.
#. Press the button *Invoices* to create the vendor bill.
#. The proposed vendor bill will be proposed for the difference between the
   received and the returned quantity.

Case 2: When you return to a supplier some products, and you have already
received a bill from the supplier.

#. Go to *Purchases > Purchase > Purchase Orders > Create*.
#. Choose a supplier and add a product whose *Invoicing Policy* is *On Received
   quantities*, and input some quantity to purchase.
#. Confirm the purchase order.
#. Go to *Shipment > Validate > Apply* so as to receive the quantities ordered.
#. Press the button *Invoices* to create the vendor bill.
#. The proposed vendor bill will be proposed for the quantity received. The
   *Invoice Status* is now 'Invoiced'
#. Go to the original incoming shipment
#. Press the button *Reverse*.
#. In the wizard *Reverse Quantity* Set *Quantity* to the quantity to be
   returned. Press *Return* to complete the wizard.
#. On the return picking press *Validate > Apply*.
#. Go back to the purchase order. It will have  *Invoice Status* as 'Waiting
   Invoces'. You will notice that the field *Received Qty* is now the quantity
   that was originally received, less the quantity that was returned.
#. Press the button *Refunds* to create the vendor refund bill.
#. The proposed vendor refund bill will be proposed for the difference between
   the received and the returned quantity.
#. If you back to the purchase order, you will notice that *Invoice Status*
   is now 'Invoiced', even when the quantity ordered does not match with the
   quantity invoiced, because you chose to refund some products.


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/95/9.0

Known issues / Roadmap
======================

* This addon is a pseudobackport of a functionality that exists natively in
  v10, plus a fix for https://github.com/odoo/odoo/issues/13974, so this addon
  will never have to be migrated to v10.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/account-invoicing/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Jordi Ballester Alomar <jordi.ballester@eficent.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
