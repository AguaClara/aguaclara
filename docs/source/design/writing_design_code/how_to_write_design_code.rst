.. _how_to_write_design_code:

How to Write Design Code
========================

Many modern programming languages (including Python) allow for the creation of
**classes**: collections of values and functions that can be accessed while
programming. This makes classes well-suited for organizing related values and
functions, but why do we have to place them in a class? Isn't it enough to just
place them in the same file?

.. code-block:: python

    class Thingy:

        # We could just as easily move these variables and functions outside of
        # the class to use them.

        a = 20
        b = 30

        def add(self):
            return self.a + self.b

        def multiply(self):
            return self.a * self.b

The answer lies in **class instantiation**!

All Python classes (with the exception of abstract classes - we'll explain that
in a bit) can be instantiated as **objects**. An object is a representative of
the class from which it comes - in other words, an *instance* of the class. It
can use all of its class's functions (also known as *methods*), while
maintaining its own set of values that may be different from the values of other
objects from the same class.

.. image:: ../../images/oop-diagram.png

Here is a general overview of how objects are used:

#. Instantiate an object from a class such that the object contains its own
   unique values.
#. Run that object's functions, which have different outcomes depending on the
   object's unique values.
#. Use multiple objects from different classes for even more different outcomes.

Python is an *object-oriented language*, where much of the language's potential
is unlocked from creating and manipulating objects. In fact, Python takes this
idea and runs with it: every single "thing" that you use in Python, like
numbers, functions, and classes, can act like an object.


This guide will show you how to write code to design a physical object, like an
AguaClara water treatment plant component. Using a Python class, this design
code will be able to take in desired parameters of the physical object, like
flow rate, and return a Python object that contains all of the necessary
physical values to build that object in real life.

This guide assumes knowledge of basic Python syntax. For a refresher, see the
`AguaClara Writing Python Code guide
<https://aguaclara.github.io/aguaclara_tutorial/python-and-hydrogen/writing-python-code.html>`_.

.. toctree::
    :maxdepth: 2

    coding_conventions
    component_class
    design_code_example
