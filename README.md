# aide_design
Design an AguaClara Water Treatment Plant with just a couple lines of code! Or just design a few components - your choice with aide_design. Aide_design parametrically designs plant components from basic physics equations. In a nutshell, you can generate a design yaml for a whole plant and print it to your console stream like so:

```python
from aide_design.play import *
from aide_render import render
import sys
my_plant = Plant(HP(30, u.L/u.s))
render(my_plant, sys.stdout)
```

## Installing
```bash
pip install aide_design
```

## Installing as a developer
If you want to make pushes to aide_design, then you should clone this repo and make the package available locally, using the following commands:
```bash
git clone https://github.com/AguaClara/aide_design.git
cd aide_design
pip install --editable . -U --user
```
The editable flag makes it so that you don't have to continuously install with pip to make the changes you just made visible.

## Updating the production version (v0.0.1 -> v0.1.0) 
We use Travis CI to automate deployment and integration. To release a new version, make a pull request to master. If the tests pass, Travis will let you merge. Once merged into master, make a tagged release. Once this tag release is pushed, Travis will rerun tests and push the source distribution (sdist) to pip at [pypi](https://pypi.org/search/?q=aide_design).

## Changelog
**aide_design design is in RAPID development. Things will shange significantly!**

We're not tracking changes at the moment here. Once development is at a more reasonable pace, we'll start tracking improvements and bug fixes more carefully!