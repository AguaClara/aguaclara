.. _install-python-pip:

=========================
Installing Python and pip
=========================

#. Download the `Anaconda installer <https://www.anaconda.com/download/>`_ and double-click it to begin installation.
#. When the installer displays Advanced Options, select "Add Anaconda to my PATH environment variable".\*

   * Aside from this, you can just click "Next" through the entire installation.

   \* If the installer did not give the option to "Add Anaconda to my PATH environment variable", follow the steps below after the installation:

   On MacOS:
    * Open the Terminal and enter ``which python``
    * Copy the directory the terminal outputs. (This is the directory Python has been installed in.)
    * Enter the command ``export PATH=$PATH<directory>``, replacing ``<directory>`` with the directory you copied above.

   On Windows:
    * Open the Command Prompt (not PowerShell) and enter ``where python``
    * Copy the path the terminal outputs. (This is the folder Python has been installed in.)
    * Enter the command ``set PATH=%PATH%;C:\path\to\python``, replacing ``C:\path\to\python`` with the path you copied above.