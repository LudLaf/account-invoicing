.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

========================
Purchase Batch Invoicing
========================

This module extends the functionality of purchases to support batch invoicing
purchase orders and to allow you to choose if you want them grouped by purchase
order or by vendor.

Configuration
=============

An automated task is included to invoice all pending purchase orders every
week, but it is disabled by default. To enable it:

#. Have *Administration / Settings* permissions.
#. Go to *Settings > Technical > Automation > Scheduled Actions > Invoice all
   pending purchase orders > Edit*.
#. Enable *Active*.
#. Save.

Usage
=====

To use this module, you need to:

#. Have *Purchase / User* permissions.
#. Go to *Purchases > Purchase > Purchase Orders > Create* and fill the form.
#. Press *Confirm*.
#. Press *Receive Products*.
#. Press *Validate > Apply*.
#. Repeat above steps a couple of times.
#. Go back to *Purchase Orders* and select those you just created.
#. Press *Action > Batch Invoice*.
#. Choose the *Grouping* method.
#. Press *Accept*.
#. You will get to a screen where you can see all the vendor bills you just
   generated.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/95/9.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/account-invoicing/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Jairo Llopis <jairo.llopis@tecnativa.com>
* Pedro Baeza <pedro.baeza@tecnativa.com>

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
