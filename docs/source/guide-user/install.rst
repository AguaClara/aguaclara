.. _install-python-pip:

Installing Python and ``pip``
=============================
1. Download the `Anaconda installer <https://www.anaconda.com/download/>`_ and double-click it to begin installation.
2. When the installer displays Advanced Options, select "Add Anaconda to my PATH environment variable".

   * Aside from this, you can just click "Next" through the entire installation.

**If the installer did not give the option to "Add Anaconda to my PATH environment variable", follow the steps below after the installation:**

On MacOS:
   3. Open the Terminal and enter ``which python``
   4. Copy the directory the terminal outputs. (This is the directory Python has been installed in.)
   5. Enter the command ``export PATH=$PATH<directory>``, replacing ``<directory>`` with the directory you copied above.

On Windows:
   3. Open the Command Prompt (not PowerShell) and enter ``where python``
   4. Copy the path the terminal outputs. (This is the folder Python has been installed in.)
   5. Enter the command ``set PATH=%PATH%;C:\path\to\python``, replacing ``C:\path\to\python`` with the path you copied above.


.. _install-git:

Installing Git
==============
On MacOS:
   1. Open the Terminal/Command Prompt and enter the following command:

      * ``git --version``

   2. If you don't alread have Git, Xcode will prompt you to install it. Follow the prompts to install Git.
   
On Windows:
   1. Download the `Git installer <https://git-scm.com/downloads>`_ and double-click it to begin installation.
   2. When the installer asks which text editor you would like to use with Git (the default is Vim), select Nano instead. While powerful, Vim is difficult to use and not necessary for Git.

      * Aside from this, you can just click "Next" through the entire installation.

3. After the installation is complete, open Terminal, PowerShell, or Command Prompt and run the two following commands with your name and the email associated with your Github account, carefully observing spaces and punctuation (including quotation marks):

   * ``git config --global user.name "Firstname Lastname"``
   * ``git config --global user.email "example@email.com"``