..
  This file documents imported variables. We must do this because autodoc
  cannot collect their docstrings.

Imported variables
==================

.. data:: eradiate.unit_registry
   :annotation: = pint.UnitRegistry()

   Unit registry common to all Eradiate components. All units used in Eradiate
   must be created using this registry.

   .. seealso:: :class:`pint.UnitRegistry`

.. data:: eradiate.unit_context_default
   :annotation: = pint.UnitContext({...})

   Unit context used when interpreting configuration dictionaries.

   .. seealso:: :class:`pinttr.UnitContext`

   .. note::

      Public interface to:

      .. autodata:: eradiate._units.unit_context_default


.. data:: eradiate.unit_context_kernel
   :annotation: = pinttr.UnitContext({...})

   Unit context used when building kernel dictionaries.

   .. seealso:: :class:`pinttr.UnitContext`

   .. note::

      Public interface to:

      .. autodata:: eradiate._units.unit_context_kernel


