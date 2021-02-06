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

### Example Usage: Design
```python
import aguaclara as ac
from aguaclara.core.units import u

# Design a water treatment plant
plant = ac.Plant(
    q = 40 * u.L / u.s,
    cdc = ac.CDC(coag_type = 'pacl'),
    floc = ac.Flocculator(hl = 40 * u.cm),
    sed = ac.Sedimentor(temp = 20 * u.degC),
    filter = ac.Filter(q = 20 * u.L / u.s)
)
```

### Example Usage: Core
```python
# continued from Example Usage: Design

# Model physical, chemical, and hydraulic properties 
cdc = plant.cdc
coag_tube_reynolds_number = ac.re_pipe(
    FlowRate = cdc.coag_q_max,
    Diam = cdc.coag_tube_id,
    Nu = cdc.coag_nu(cdc.coag_stock_conc, cdc.coag_type)
)
```

### Example Usage: Research
```python
import aguaclara as ac
from aguaclara.core.units import u
import matplotlib.pyplot as plt

# Plan a research experiment
reactor = ac.Variable_C_Stock(
    Q_sys = 2 * u.mL / u.s, 
    C_sys = 1.4 * u.mg / u.L, 
    Q_stock = 0.01 * u.mL / u.s
)
C_stock_PACl = reactor.C_stock()

# Visualize and analyze ProCoDA data
ac.iplot_columns(
    path = "https://raw.githubusercontent.com/AguaClara/team_resources/master/Data/datalog%206-14-2018.xls", 
    columns = [3, 4], 
    x_axis = 0
)
plt.ylabel("Turbidity (NTU)")
plt.xlabel("Time (hr)")
plt.legend(("Influent", "Effluent"))
```

The package is still undergoing rapid development. As it becomes more stable, a user guide will be written with more detailed tutorials. At the moment, you can find some more examples in specific pages of the [API reference](https://aguaclara.github.io/aguaclara/api.html).

## Contributing
Bug reports, features requests, documentation updates, and any other enhancements are welcome! To suggest a change, [make an issue](https://github.com/AguaClara/aguaclara/issues/new/choose) in the [`aguaclara` Github repository](https://github.com/AguaClara/aguaclara>).

To contribute to the package as a developer, refer to the [Developer Guide](https://aguaclara.github.io/aguaclara/guide-dev/guide-dev.html).
