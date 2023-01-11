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
# Functions to read in data and get other things.


def read_exoplanetA():
    '''
    Function to read in data from exoplanetA.
    '''
    data_path = f"{main_path}/exoplanet_2023A_data.txt"
    data = pd.read_csv(data_path, sep='\s+', skiprows=13, names=column_names)
    # getting full number, see data file for explaination.
    data[molecules_names] *= 1e22
    return data


def get_num_densities(data=None, molecules_names=molecules_names):
    '''
    Function to get the number densities of compounds in some data.
    '''
    if not data:
        data = read_exoplanetA()

    return data[molecules_names]


def calc_mass_density(num_density, molar_mass):
    '''
    Function to calculate the mass density from the number density and molar mass of a given element/compound.
    '''
    return (num_density*molar_mass)/constants.Avogadro


# *************************************************************************************


def plot_vs_pressure(x, y, title, xlabel, *args):
    '''
    Function to make plots againist pressure
    '''
    plt.plot(x, y)
    plt.gca().invert_yaxis()

    plt.title(title, fontsize=14)
    plt.ylabel("Pressure $[Pa]$")
    plt.xlabel(xlabel)
