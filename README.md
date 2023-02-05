# Python Library specfically for Phys 340 Atmosphere physics

<br>

How to import functions and variables:
```py
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
```

<br>

The `Calculator.ipynb` file needs to be moved outside the `Phys340PyPackages` folder. Otherwise the import paths of the modules will not work.<br><br>
Same with the data file `exoplanet_2023A_data.txt`, which can be found in the `myData` folder. <br>

**Filetree**:<br>
Folder ->
- Phys340PyPackages
- Calculatoy.ipynb
- exoplanet_2023A_data.txt


