New API documentation
=====================

..
  The following toctree contains documentation generated manually because
  autosummary can't do the job correctly.

.. toctree::
   :hidden:

   imported_vars

Mode control
------------

.. currentmodule:: eradiate

.. autosummary::
   :toctree: generated/

   mode
   modes
   set_mode

Units
-----

.. currentmodule:: eradiate

.. list-table::
   :widths: 1 3

   * - :data:`unit_registry`
     - Unit registry common to all Eradiate components.
   * - :data:`unit_context_default`
     - Unit context used when interpreting configuration dictionaries.
   * - :data:`unit_context_kernel`
     - Unit context used when building kernel dictionaries.

Miscellaneous
-------------

.. autosummary::
   :toctree: generated/

   __version__
