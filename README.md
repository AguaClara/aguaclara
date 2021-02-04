# `aguaclara`
[![Pypi Version](https://img.shields.io/pypi/v/aguaclara?color=blue&label=PyPI)](https://pypi.org/project/aguaclara/)
[![Documentation](https://github.com/AguaClara/aguaclara/workflows/Documentation/badge.svg)](https://aguaclara.github.io/aguaclara/) 
[![Build Status](https://github.com/AguaClara/aguaclara/workflows/Build/badge.svg)](https://github.com/AguaClara/aguaclara/actions) 
[![Code Coverage](https://codecov.io/gh/AguaClara/aguaclara/branch/master/graph/badge.svg)](https://app.codecov.io/gh/AguaClara/aguaclara/)

`aguaclara` is a Python package developed by [AguaClara Cornell](http://aguaclara.cornell.edu/) and [AguaClara Reach](https://www.aguaclarareach.org/) for designing and performing research on AguaClara water treatment plants. The package has several main functionalities:

* **DESIGN** of AguaClara water treatment plant components
* **MODELING** of physical, chemical, and hydraulic processes in water treatment
* **PLANNING** of experimental setup for water treatment research
* **ANALYSIS** of data collected by [ProCoDA](https://monroews.github.io/EnvEngLabTextbook/ProCoDA/ProCoDA.html) (process control and data acquisition tool)


## Installing
The `aguaclara` package can be installed from Pypi by running the following command in the command line:

```bash
pip install aguaclara
```
To upgrade an existing installation, run 

```bash
pip install aguaclara --upgrade
```

## Using `aguaclara`
`aguaclara`'s main functionalities come from several sub-packages.

1. **Core**: fundamental physical, chemical, and hydraulic functions and values
2. **Design**: modules for designing components of an AguaClara water treatment plant
3. **Research**: modules for process modeling, experimental design, and data analysis in AguaClara research

To use `aguaclara`'s registry of scientific units (based on the [Pint package](https://pint.readthedocs.io/en/latest/)), use `from aguaclara.core.units import u`. Any other function or value in a sub-package can be accessed by importing the package itself:

```python
import aguaclara as ac
from aguaclara.core.units import u

ac.viscosity_kinematic(20 * u.degC)
```

The package is still undergoing rapid development. As it becomes more stable, user guides will be written to demonstrate each of these main functionalities.
At the moment, you can find some examples in specific pages of the [API reference](https://aguaclara.github.io/aguaclara/api.html).

## Contributing
Bug reports, features requests, documentation updates, and any other enhancements are welcome! To suggest a change, [make an issue](https://github.com/AguaClara/aguaclara/issues/new/choose) in the [`aguaclara` Github repository](https://github.com/AguaClara/aguaclara>).

To contribute to the package as a developer, refer to the [Developer Guide](https://aguaclara.github.io/aguaclara/guide-dev/guide-dev.html).
