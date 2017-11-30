dgp\.gui package
================

GUI Design Notes
----------------

*DRAFT*
Models, Views and dgp.lib.types

Many of DGP's UI components utilize the Qt Model/View methodology and
components provided by the Qt/PyQt framework.
To this end, the dgp.lib.types module provides several abstract and base
classes that are designed to be subclassed by arbitrary user defined types
within the project structure.

These base types provide the basic implementation for the subclass to be
displayed in a Qt View item, with minimal boilerplate code required in the
subclass. Typically the subclasses must only override or extend the data()
method of the base type, in order to display relevant visual data.


Submodules
----------

dgp\.gui\.models
----------------

.. automodule:: dgp.gui.models
   :members:
   :undoc-members:
   :show-inheritance:

dgp\.gui\.utils
----------------

.. automodule:: dgp.gui.utils
   :members:
   :undoc-members:
   :show-inheritance:


dgp\.gui\.qtenum
----------------

.. automodule:: dgp.gui.qtenum
   :members:
   :undoc-members:
   :show-inheritance:
