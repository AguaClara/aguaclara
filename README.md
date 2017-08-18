# aide_design
Contains all design files for the AguaClara Infrastructure Design Engine (AIDE). This package can take user-defined parameters specified in the design() function and generate a class of the particular unit process designed with all relevant dimensions determined. The class is easily serializable as a JSON. 

# Installing with pip
If you'd like to install across your whole machine, you can open the cmd (Windows) or teminal (mac) and type `$pip install aide_design`. If you get a permission denied error, you probably want to install it instead to your particular user with `$pip install aide_design --user`.

# Installing as a developer
If you want to be able to edit the source code, you need to clone this repo with git, then run the 'setup.py' folder in the top level directory: `python setup.py install`. Whenever you make a change to the code, you need to run this command to ensure that the change has been successfully packaged.
