.. _guide-dev:

.. |aguaclara Github| replace:: ``aguaclara`` Github repository
.. _aguaclara Github: https://github.com/AguaClara/aguaclara

.. |aguaclara issues| replace:: ``aguaclara`` Github repository issues
.. _aguaclara issues: https://github.com/AguaClara/aguaclara/issues

===============
Developer Guide
===============

Where to Start
--------------
Whether you're are maintainer of ``aguaclara`` or a user with a bug fix, feature, or enhancement in mind, the |aguaclara issues|_ are a great place to start. 

Before working, **browse the issues to check if the update you have in mind has already been documented and assigned to a developer**. If a relevant issue doesn't exist, go ahead and make one with the green button labeled "New Issue". If/once an issue does exist, there a few ways to proceed:

* if you're a collaborator of the ``aguaclara`` repository, assign yourself to the issue.
* if you're not a collaborator, either ask a collaborator to make you a collaborator as well, or ask the collaborator to assign you to the issue.

Feel free to use the issue for commenting on your progress or asking other users or collaborators for help with your development.


Setting Up Your Local Environment
---------------------------------
If you want to make changes to ``aguaclara``, you should make the package available locally.

#.  Make sure to have Python, ``pip``, and Git installed (for guidance, see :ref:`install-python-pip`). The ``aguaclara`` package requires Python versions [COME BACK HERE WITH RIGHT VERSIONS]. If you must have a different version on your computer for another project, refer to the ``pyenv`` tutorial [WRITE THIS LATER] for managing multiple Python versions.

#.  Install `Pipenv <https://pypi.org/project/pipenv/>`_, a package management and virtual environment tool, by running the following command in the command line:
   
    .. code:: 
    
        pip install pipenv

#.  In the command line, navigate to the directory in which you'll keep your local copy of the ``aguaclara`` Git repository.
   
    * If you're not a collaborator, you'll need to first fork the repository on Github.

#.  Clone the repository or your fork of the repository into that directory:

    .. code::
        
        (Cloning original repository)
        git clone https://github.com/AguaClara/aguaclara.git

        (Cloning forked repository)
        git clone https://github.com/{your_username_here}/aguaclara.git
    
#.  Navigate into the newly cloned repository and install it in editable mode, so that your environment uses this repository as your ``aguaclara`` package, even as you edit it:

    .. code::

        cd aguaclara
        pip install --editable . -U --user

#.  Install the package's user dependencies and development dependencies:

    .. code::

        pipenv install
        pipenv install --dev
    
    ``pipenv`` is used to install the dependencies from the file called ``Pipfile`` into a virtual environment. Click :ref:`here <pipenv>` for more details on ``pipenv`` and ``Pipfile``. 

#.  You can check whether you have a working testing environment by running:

    .. code::

        pipenv run pytest
    
    The tests should all pass. If they don't, check in with the latest `Github Actions build of the master branch <https://github.com/AguaClara/aguaclara/actions?query=branch%3Amaster>`_ to see what difference between the Github Actions environment and your local environment could make the tests fail.


Branching
---------
Before you develop, it's important to understand the branching conventions for the ``aguaclara`` repository.

The Master Branch
*****************
The master branch is the branch that houses ``aguaclara``'s published releases. Therefore, the master branch is a *protected* with rules (on Github) that

* pull requests are required before merging into the branch,
* only administrators and maintainers can push to the branch, and
* status checks are required before merging or pushing to the branch.

Your Development Branch
***********************
This means that all work starts on *development branches* (or task, feature, or release branches. Check out this `article <https://www.atlassian.com/agile/software-development/branching>`_ if you want to learn more!)
It is recommended that you name your branch ``{your_development_type}/short-description``. Some examples of development type are 

.. hlist::
    :columns: 2

    * ``feature``
    * ``bugfix``
    * ``enhancement``
    * ``documentation``
    * ``test`` (for additions/updates to tests)
    * ``build`` (for updates to the build process)

To make and switch to your new branch, run:

.. code::

    git checkout -b {your_development_type}/short-description

Documentation and Test Driven Development
-----------------------------------------
