# Python Library specfically for Phys 340 Atmosphere physics

<br>

How to import functions and variables:
```py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import constants

# Custom Packages
from Phys340PyPackages import (
    molecules_names,
    molar_mass,
    column_names
)
from Phys340PyPackages import ( 
    read_exoplanetA,
    get_num_densities,
    get_mass_density,
    get_mass_fraction,
    get_specific_humidity
)
from Phys340PyPackages import (
    plot_vs_pressure
)