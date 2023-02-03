import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import constants

main_path = '../../Data/'

# *********************** Parameters ***********************

molecules_names = ['N2', 'CO', 'O2', 'H2', 'Ar', 'H2O']
column_names = ['pressure', 'temperature', 'air_density',
                'zonal_wind', 'merid_wind'] + molecules_names
molar_mass = {
    # molar mass, in  Kg/mol
    'dry_air' : 28.9647e-3,
    'wet_air' : 18e-3,
    "N2": 28.013e-3,
    'CO': 28.010e-3,
    'O2': 32e-3,
    'H2': 2.016e-3,
    'Ar': 39.948e-3,
    'H2O': 18.015e-3
}


# *********************** Functions ***********************

def read_exoplanetA():
    '''
    Function to read in data from exoplanetA.
    '''
    data_path = f"{main_path}/exoplanet_2023A_data.txt"
    data = pd.read_csv(data_path, sep='\s+', skiprows=13, names=column_names)
    # getting full number, see data file for explaination.
    data[molecules_names] *= 1e22
    return data


def read_num_densities(data=None, molecules_names=molecules_names):
    '''
    Function to read the number density of compounds from some data.
    Returns DataFrame.
    '''
    if not data:
        data = read_exoplanetA()

    return data[molecules_names]
