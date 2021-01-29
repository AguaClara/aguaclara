===============================================
Welcome to the AguaClara Package Documentation!
===============================================

.. image:: images/logo.png
    :align: center

``aguaclara`` is a Python package that assists the development of `AguaClara <https://www.aguaclarareach.org/>`_ sustainable water treatment technology. The package has several main functionalities:

* **DESIGN** of AguaClara water treatment plant components
* **MODELING** of physical, chemical, and hydraulic processes in water treatment
* **PLANNING** of experimental setup for water treatment research
* **ANALYSIS** of data collected by `ProCoDA <https://monroews.github.io/EnvEngLabTextbook/ProCoDA/ProCoDA.html>`_ (process control and data acquisition tool)

.. The package is still undergoing rapid development. As it becomes more stable, user guides will be written to demonstrate each of these main functionalities.
.. At the moment, you can find some examples in specific pages of the API reference.

Installing
----------
The ``aguaclara`` package can be installed from `Pypi <https://pypi.org/project/aguaclara/>`_ by running the following command in the command line: 

.. code::

  pip install aguaclara

To upgrade an existing installation, run 

.. code::

  pip install aguaclara --upgrade

Click here for :ref:`more software installation instructions <install-python-pip>` if you don't have Python or pip installed yet.

Using ``aguaclara``
-------------------
``aguaclara``'s main functionalities come from several sub-packages.

1. **Core**: fundamental physical, chemical, and hydraulic functions and values
2. **Design**: modules for designing components of an AguaClara water treatment plant
3. **Research**: modules for process modeling, experimental design, and data analysis in AguaClara research

To use ``aguaclara``'s registry of scientific units (based on the `Pint package <https://pint.readthedocs.io/en/latest/>`_), use ``from aguaclara.core.units import u``. Any other function or value in a sub-package can be accessed by importing the package itself:

.. code-block:: python

  import aguaclara as ac
  from aguaclara.core.units import u

  ac.viscosity_kinematic(20 * u.degC)

For more detailed tutorials and examples on using the package, refer to the :ref:`User Guide <guide-user>`.

Contributing
------------
To report a bug or request or feature, make an issue in the `AguaClara package Github repository <https://github.com/AguaClara/aguaclara>`_.

For more detailed tutorials on contributing to the package, refer to the :ref:`Developer Guide <guide-dev>`.

Table of Contents
-----------------
.. toctree::
    :maxdepth: 1

    guide-user/guide-user
    guide-dev/dev-intro
    api
