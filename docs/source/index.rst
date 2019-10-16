===============================================
Welcome to the AguaClara Package Documentation!
===============================================

.. image:: images/logo.png
    :align: center

``aguaclara`` is a Python package built by `AguaClara Cornell <http://aguaclara.cee.cornell.edu/>`_ for AguaClara water treatment plant design and research.

Installing
----------
The ``aguaclara`` package can be installed by running ``pip install aguaclara`` in the command line. To upgrade an existing installation, run ``pip install aguaclara --upgrade``.

Contributing
------------
To report a bug or request or feature, make an issue in the `AguaClara package Github repository <https://github.com/AguaClara/aguaclara>`_.

Using ``aguaclara``
-------------------
``aguaclara`` is organized into three sub-packages.

1. **Core**: fundamental physical, chemical, and hydraulic functions and values
2. **Design**: modules for creating a parameterized design of an AguaClara water treatment plant
3. **Research**: modules for process modeling, experimental design, and data analysis in AguaClara research

To use ``aguaclara``'s registry of scientific units (based on the `Pint package <https://pint.readthedocs.io/en/latest/>`_), use ``from aguaclara.core.units import u``. Any other function or value in a sub-package can be accessed by importing the package itself:

.. code-block:: python

  import aguaclara as ac
  from aguaclara.core.units import u

  ac.viscosity_kinematic(20 * u.degC)

``aguaclara`` Reference
-----------------------
The following pages document the modules, functions, and values available in each sub-package.

.. toctree::
    :maxdepth: 2

    core/core
    design/design
    research/research
