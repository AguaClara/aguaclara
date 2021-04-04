===================
Units
===================

Units are something that every researcher using the AguaClara Package will use! Our `Units module <https://aguaclara.github.io/aguaclara/core/units.html>`_ is based off on the `Pint package <https://pint.readthedocs.io/en/latest/>`_, so make sure to check them out if you need any additional information. 

Quick Start
~~~~~~~~~~~
First, import the Units module. You can name it anything you want, but we will use ``u`` here since it's easy to type.

.. code-block:: python

    >>> from aguaclara.core.units import u


To add units to a variable, simply multiply ``*`` or ``/`` divide it, as you would with regular numbers or variables. Similarly, you can use ``**`` if you want to raise a unit to a power. 


.. code-block:: python

    >>> distance = 10 * u.m
    >>> speed = 2.5 * u.m / u.s
    
    >>> area1 = (8 * u.m) ** 2
    >>> area2 = 64 * u.m * u.m
    >>> print("Is area1 is equal to area 2? " + str(area1 == area2))
    area1 is equal to area 2? True
    

As expected, units hold for multiplication and division. Addition and subtraction will only work if the units are of the same dimension. 

.. code-block:: python

    >>> time = distance / speed
    >>> print(time)
    4 second 


    >>> print(time + 1 * u.ms)
    4.001 second
    >>> print(distance + speed)
    DimensionalityError: Cannot convert from 'meter' ([length]) to 'meter / second' ([length] / [time])


To convert between units, we can use ``to(newunits)``, where ``newunits`` is your desired units. If you try to convert between different dimensions, you will get a ``DimensionalityError``. Another way to convert units is ``to_base_units()``.

.. code-block:: python

    >>> length = 100 * u.cm 
    >>> print(length)
    100 centimeter

    >>> print(length.to_base_units())
    1 meter

    >>> print(length.to(u.s))
    DimensionalityError: Cannot convert from 'centimeter' ([length]) to 'second' ([time])


To get the magnitude: 

.. code-block:: python

    >>> a = 3.235 * u.m
    >>> print(a)
    3.235 meter
    >>> print(a.magnitude)
    3.235


Constants
~~~~~~~~~

The module also includes some `constants <https://aguaclara.github.io/aguaclara/core/units.html#constants>`_. To use them, you can multiply or divide them similarly as you would with other values. 

Constants are actually 'Unit' objects, so they will appear differently, for example, ``standard_gravity``. You can convert it to "normal" units using ``to()`` or ``to_base_units()`` after your calculations. Note: you cannot convert the actual constant to base units because it is a Unit object, not a value. 

.. code-block:: python

    >>> print(u.gravity)
    standard_gravity
    >>> print(u.gravity.to_base_units())
    AttributeError: 'Unit' object has no attribute 'to_base_units'
    >>> print((u.gravity * 1).to_base_units()) 
    9.807 meter / second ** 2

    >>> F = 1.5*u.kg * u.gravity
    >>> print(F)
    1.5 kilogram * standard_gravity
    >>> print(F.to_base_units())
    14.71 kilogram * meter / second ** 2
    >>> print(F.to(u.kg * u.m / u.s**2))
    14.71 kilogram * meter / second ** 2


Sig-Figs
~~~~~~~~

Significant figures are also very important in calculations. ``set_sig_figs(n)``  allows you to display only ``n`` significant figures when you print a value that has units. 

.. code-block:: python
    
    >>> print(4/7 * u.m)
    0.5714 meter
    >>> ac.set_sig_figs(6)
    >>> print(4/7 * u.m)
    0.571429 meter


Using Units with Other Data Structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Units also work with other data structures. Let's look at lists, NumPy arrays, and tuples for now, but you can definitely attach units to other structures as well!

.. code-block:: python

    >>> lst = [1,2,3] * u.m 
    >>> print(lst)
    [1 2 3] meter

    >>> arr = np.array([1,2,3]) * u.m
    >>> print(arr)
    [1 2 3] meter

    >>> tup = (3*u.m, 5*u.m)
    >>> print(tup) 
    (<Quantity(3, 'meter')>, <Quantity(5, 'second')>)

    >>> tup = (3, 5) * u.s
    >>> print(tup)
    [3 5] second

Most commonly, we will attach units on the outside of the structure (ex: ``[1,2]*u.s``) so that we can remove units easily if needed. 

.. code-block:: python

    >>> arr = [1,2,3] * u.m
    >>> print(arr)
    [1 2 3] meter
    >>> print(arr / u.m)
    [1 2 3] dimensionless

However, this does not work for pandas series. If you want to attach units to pandas series, it must be attached to individual elements rather than outside of the structure. 

.. code-block:: python

    >>> a = pd.Series([1*u.min, 2*u.min, 3*u.min])  // works
    >>> print(a)
    0    1 minute
    1    2 minute
    2    3 minute
    dtype: object

    >>> b = pd.Series([1, 2, 3]) * u.min            // will not work
    >>> print(b)
    0    1
    1    2
    2    3
    dtype: int64
    UnitStrippedWarning: The unit of the quantity is stripped when downcasting to ndarray.

    >>> c = pd.Series([1, 2, 3] * u.min)            // will not work
    >>> print(c)
    0    1
    1    2
    2    3
    dtype: int64
    UnitStrippedWarning: The unit of the quantity is stripped when downcasting to ndarray.


That's all we have for Units at the moment! Check out the `Pint package <https://pint.readthedocs.io/en/latest/>`_ for more information! 

