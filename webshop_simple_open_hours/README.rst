=====================================
  Webshop Simplified Open Hours
=====================================

This module is an add-on to ``webshop_simple``.

It creates configuration entries for setting open business hours.

This module overrides the cart update endpoint in order to check if order is passed during working hours.

Configuring open hours is done on the company level where you can set:

- Timezone

- Closing hour on J: an order passed before this our will be processed today

- Opening hour on J+1: an order passed after this our will be processed the day after

Adding to cart is only available each day outside of this interval set.



Installation notes
==================

Credits
=======

Contributors
------------

* Paul Ntabuye Butera <paul.n.butera@abakusitsolutions.eu>
* Valentin Thirion <valentin.thirion@abakusitsolutions.eu>

Maintainer
-----------

.. image:: http://www.abakusitsolutions.eu/wp-content/themes/abakus/images/logo.gif
   :alt: AbAKUS IT SOLUTIONS
   :target: http://www.abakusitsolutions.eu

This module is maintained by AbAKUS IT SOLUTIONS