
# This module is specific to one dataset "exoplanet_2023A_data.txt"

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import constants

# *************************************************************************************
# System Parameters

main_path = '../../Data/'

# *************************************************************************************
# data parameters

molecules_names = ['N2', 'CO', 'O2', 'H2', 'Ar', 'H2O']
column_names = ['pressure', 'temperature', 'air_density',
                'zonal_wind', 'merid_wind'] + molecules_names
molar_mass = {
    # molar mass, in  Kg/mol
    "N2": 28.013e-3,
    'CO': 28.010e-3,
    'O2': 15.999e-3,
    'H2': 2.016e-3,
    'Ar': 39.948e-3,
    'H2O': 18.015e-3
}

# *************************************************************************************
# Functions to read in data


def read_exoplanetA():
    '''
    Function to read in data from exoplanetA.
    '''
    data_path = f"{main_path}/exoplanet_2023A_data.txt"
    data = pd.read_csv(data_path, sep='\s+', skiprows=13, names=column_names)
    # getting full number, see data file for explaination.
    data[molecules_names] *= 1e22
    return data


# *************************************************************************************
# Functions for calculating

def get_num_densities(data=None, molecules_names=molecules_names):
    '''
    Function to get the number density of compounds in some data.
    Returns DataFrame.
    '''
    if not data:
        data = read_exoplanetA()

    return data[molecules_names]


def get_mass_density():
    '''
    Function to calculate the mass density from the number density and molar mass of a given element/compound.
    Returns DataFrame.
    '''
    def mass_density(num_density, molar_mass): 
        return (num_density*molar_mass)/constants.Avogadro

    return pd.concat([mass_density(get_num_densities()[name], molar_mass[name])
                      for name in molecules_names], axis=1)


def get_specific_humidity(data=None):
    '''
    Function to calculate the specific humidity.
    Returns pd Series.
    '''
    if not data:
        data = read_exoplanetA()
    water_vapour_density = get_mass_density(data.H2O, molar_mass['H2O'])
    return water_vapour_density/data.air_density


# *************************************************************************************


def plot_vs_pressure(x, title, xlabel, *args):
    '''
    Function to make plots againist pressure
    '''
    plt.plot(x, read_exoplanetA().pressure, args)
    plt.gca().invert_yaxis()

    plt.title(title, fontsize=14)
    plt.ylabel("Pressure $[Pa]$")
    plt.xlabel(xlabel)
