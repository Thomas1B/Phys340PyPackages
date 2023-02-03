
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
    'dry_air' : 28.9647e-3,
    "N2": 28.013e-3,
    'CO': 28.010e-3,
    'O2': 32e-3,
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
data = read_exoplanetA()

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


def get_mass_density(name=None):
    '''
    Function to calculate the mass density from the number density and molar mass of a given element/compound.

    Parameter:
        name (str): Optional, name of compound.

    Returns:
        if name parameter is given -> Series.
        otherwise -> DataFrame.
    '''

    def mass_density(num_density, molar_mass): 
        return (num_density*molar_mass)/constants.Avogadro

    if name:
        return pd.Series(mass_density(get_num_densities()[name], molar_mass[name]), name=name)
    else:
        return pd.concat([mass_density(get_num_densities()[name], molar_mass[name])
                      for name in molecules_names], axis=1)


def get_specific_humidity():
    '''
    Function to calculate the specific humidity.
    Returns pd Series.
    '''
    water_vapour_density = get_mass_density('H2O')
    return pd.Series(water_vapour_density/data.air_density, name="specific_humidity")


def get_mass_fraction(name=None):
    '''
    Parameter:
        name (str): Optional, name of compound.

    Returns:
        if name parameter is given -> Series.
        otherwise -> DataFrame.
    '''

    if name:
        return pd.Series(get_mass_density(name)/data.air_density, name=name)
    else:
        mass_density = get_mass_density()
        mass_fraction = pd.concat([mass_density[name]/data.air_density
                                for name in mass_density], axis=1)
        mass_fraction.columns = mass_density.columns
        return mass_fraction


def Clau_Clap_eqn(T, L=2.45e6):
    '''
    Function to calculate the saturation vapour pressure over a flat surface
    using the Clausius-Clapeyron equation.

    Parameters:
        T (float): temperature in kelvin.
        L (optional): Specific enthalpy, default -> vapourization.

    Returns:
        pressure in hPa.
    '''
    k = (0.018*L)/8.315
    return 6.11*np.exp(k*(273**-1 - T**-1))


def dewpoint_temp(e, e0, L=2.45e6):
    '''
    Function to calculate the dewpoint temperature.

    Parameters:
        e - final vapour pressure.
        e0 - initial vapour pressure.
        L (optional): Specific enthalpy, default -> vapourization.
    
    Returns:
        temperature in kelvin.
    '''
    k = 8.315/(0.018*L)
    return 1/(273**-1 - k*np.log(e/e0))



def kelvin_eqn(r, T):
    '''
    Function to calculate the saturation vapour pressure for a droplet of radius using the kelvin equation.

    Parameters:
        r (float) radius of droplet.
        T (float) temperature
    '''
    sigma = 0.0720 # water surface tension.
    return Clau_Clap_eqn(T)*np.exp((2*18e-3*sigma)/(r*1e3*constants.gas_constant*T))


# *************************************************************************************


def plot_vs_pressure(x, title=None, xlabel=None, label=None, kind=None):
    '''
    Function to make plots againist pressure
    '''
    if kind:
        if kind == "semilogx": plt.semilogx(x, read_exoplanetA().pressure/100, label=label)
        elif kind == "semilogy": plt.semilogy(x, read_exoplanetA().pressure/100, label=label)
        elif kind == "loglog": plt.loglog(x, read_exoplanetA().pressure/100, label=label)
    else:
        plt.plot(x, read_exoplanetA().pressure/100, label=label)

    plt.gca().invert_yaxis()
    plt.title(title, fontsize=14)
    plt.ylabel("Pressure $[hPa]$")
    plt.xlabel(xlabel)
    plt.grid()