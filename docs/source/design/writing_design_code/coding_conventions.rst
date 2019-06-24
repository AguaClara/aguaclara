.. _coding-conventions:

Coding Conventions
==================

Outside of Python classes, writing Python code is relatively straightforward.
You call or write functions that run calculations, then use those calculations
in future calculations until you reach your desired outcome. However, Python
classes aren't as linear - they utilize the concept of object-oriented
programming (OOP), where functionality stems from creating and manipulating
Python objects. Python classes become strongly fixed within your code - they
will be used more widely than functions at times, and may deviate wildly from
code that other people write. That is why it's important to write good design
code - so that other engineers know how to use it the way you intended!

There are 4 general concepts that you should follow when writing design code:

#. Clarity over comments
#. Useful names
#. Avoiding redundancy
#. Other tips

Clarity over comments
------------------------

Suppose you want to assign the value of a flocculator's channel length to a
variable. Some people would just give a very short, basic name to avoid typing
too much in the future:

.. code-block:: python

    # Flocculator channel length maximum
    a = 6 * u.m

This does seem to be pretty clear when the variable is defined, but consider
what happens when you want to use that variable elsewhere in your code. It
becomes easy to forget what ``a`` signifies, and if someone were to begin
reading code below where ``a`` is defined, they would be confused and not know
what it represents.

Instead, variable names should be descriptive on their own:

.. code-block:: python

    floc_chan_l_max = 6 * u.m

This mitigates all of the problems of the ``a`` variable name, even though it is
longer. Furthermore, someone who is reading the code will immediately know what
the variable represents, regardless of the context. While it is perfectly fine
to use comments when writing complex equations or logic, they should be used
sparingly.

**Main takeaway:** as often as possible, write code that doesn't require the use
of comments to be understandable.

Useful names
--------------------

When reading ``floc_chan_l_max``, you should have a good idea of what it
represents: the flocculator's channel length's maximum. But why can we
abbreviate it like so, instead of calling it
``flocculator_channel_length_maximum``, and why is it not ordered as
``l_max_floc_chan`` instead?

Abbreviations
^^^^^^^^^^^^^

In the `Design Variable Naming Conventions spreadsheet
<https://aguaclara.github.io/aguaclara_tutorial/python-and-hydrogen/writing-python-code.html>`_,
all of the standard variable names (as well as their dimension/type and
abbreviations) are listed out. For example, the spreadsheet lists out the
abbreviations for "flocculator", "channel", "length", and "maximum", which were
used in ``floc_chan_l_max``.

When creating a variable, familiarize yourself with the relevant names and
abbreviations, then use them in the variable - using these standard
abbreviations makes it easy for others to understand your code without it
becoming too verbose!

Ordering
^^^^^^^^

Names should be ordered to follow a hierarchy of "largest-to-smallest":

#. Component (``floc``)
#. Subcomponent (``chan``)
#. Parameter (``l``)
#. Descriptor (``max``)
#. Other descriptors

This hierarchy is used to intuitively group together similar variables, and to
make them easier to translate into plain English.

Suppose we also wanted to define another variable for the minimum width of the
flocculator channel. Disregarding the ordering hierarchy would lead to:

.. code-block:: python

    min_w_chan_floc = 42 * u.inch
    l_max_floc_chan = 6 * u.m

If we instead follow the ordering hierarchy, it becomes easier to see at a
glance that these variables refer to different parameters of the same component:

.. code-block:: python

    floc_chan_w_min = 42 * u.inch
    floc_chan_l_max = 6 * u.m

A good way to validate whether your names follow the correct order is to place
"*'s*" after each word except for the last one and see if the phrase still makes
sense in plain English. For example, ``floc_chan_l_max`` is still grammatical as
*the flocculator's channel's width's maximum*

**Main takeaway:** strike a balance between ease of use and descriptiveness when
writing variable names.

Avoid redundancy
-------------------

On its own, a variable called ``floc_chan_w_max`` makes sense in a general
context. However, Python objects will need to store their own variables (also
known as fields or properties) for a user to call upon them. The
:class:`aguaclara.design.floc.Flocculator` class contains a property for the
channel width's maximum, but if it were to be named as ``floc_chan_w_max``
within the class, using the property would become clunky:

.. code-block:: python

    floc = Flocculator(q = 30 * u.L / u.s)
    print(floc.floc_chan_w_max)

Within the class, we already *know* that this property belongs to the
flocculator, so there isn't a need to add the word ``floc`` to the variable name
when writing the class:

.. code-block:: python

    floc = Flocculator(q = 30 * u.L / u.s)
    print(floc.chan_w_max)

This concept applies well to when we want to compose multiple different
components together, like the Entrance Tank/Flocculator Assembly (see
:class:`aguaclara.design.ent_floc.EntTankFloc`):

.. code-block:: python

    etf = EntTankFloc(q = 30 * u.L / u.s)
    print(etf.floc.chan_w_max)

**Main takeaway:** consider the context in which variables are used.

Other tips
-------------

Module/class naming
^^^^^^^^^^^^^^^^^^^

Modules (Python files in which you store your classes) should be named according
to the `Design Variable Naming Conventions spreadsheet
<https://aguaclara.github.io/aguaclara_tutorial/python-and-hydrogen/writing-python-code.html>`_
(``floc.py``), and classes should be named fully in plain English
(``Flocculator``). The exception to class naming is when they become excessively
long (``EntranceTankFlocculatorAssembly``) - in that case, use abbreviations
whenever possible so that the name is easy to understand and descriptive
(``EntTankFloc``).

Line length
^^^^^^^^^^^

To avoid having overly long lines, try to keep them below 80 characters long.
Atom shows your line length in the bottom left corner.