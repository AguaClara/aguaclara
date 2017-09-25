# aide_design
Contains all design files for the AguaClara Infrastructure Design Engine (AIDE). This package can take user-defined 
parameters specified in the design() function and generate a class of the particular unit process designed with all 
relevant dimensions determined. The resulting unit process class is easily serializable as a JSON. 

## Installing
1. Ensure you have Anaconda installed
2. Create a virtual environment named aide_design: `$conda create --name aide_design` These are very handy and safegaurd against compatability issues.
3. Activate the newly created environment: 
        a. Windows: `$activate aide_design`
        b. macOS and Linux: `$source activate aide_design`
4. Install aide_design and it's dependencies using pip: `$pip install aide_design`

**Note** It is preferred to install from conda. As a backup, use pip. See below for more in depth expanation about pip v. conda.

### Conda
TODO
### Pip 
* You will probably want to install from pip, where we host the latest production package. If you downloaded Anaconda, 
you'll already have pip installed. The following is how to install with pip:
* If you'd like to install across your whole machine, you can open the cmd (Windows) or teminal (mac) and type 
`$pip install aide_design` (where $ signifies the beginning of the command.) If you get a permission denied error, you 
probably want to install it instead to your particular user with `$pip install aide_design --user`. This will install 
the latest 

## Installing as a developer
If you want to be able to edit the source code, you need to clone this repo with git, then run the 'setup.py' folder 
in the top level directory with pip: `$pip install . -U`. Whenever you make a change to the code, you need to run this 
command to ensure that the change has been successfully packaged. Now you should be able to import aide_design 
into python: `import aide_design`

## Updating the production version (v0.0.1 -> v0.1.0) 
When the master branch updates with some new Pull Requests, there are several steps that need to be taken to keep all 
the production outlets in sync. Here are the steps:
1. Create a tagged release on Github to signify this version of the code is in production: 
    * The tag should use the [semantic versioning](http://semver.org/) naming convention (MAJOR.MINOR.PATCH). 
    * Once you determined the correct tag, be sure to update the setup.py metadata to explicitly state the version number.
    * To tag the current commit, use the create annotated tag command: `$git tag -a v1.4.0 -m "my version 1.4.0"`
    * Make sure to push to GitHub!
2. Now you need to push the distribution to pip test and pip live websites:
    * Make sure you have a [.pypirc](https://docs.python.org/2/distutils/packageindex.html#the-pypirc-file) in your home 
    folder with the correct username and password (available on the drive in the passwords doc)
    * Now you should build the distribution and upload to pip with `$python setup.py sdist bdist_wininst upload`
3. Make sure your new package works:
    * Update your package through pip and ensure the version number has changed: `$pip install aide_design --upgrade` 
    and `$pip list` 
    * If the version number now matches, you've successfully upgraded the pip package. 
