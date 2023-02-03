
# This module is specific to one dataset "exoplanet_2023A_data.txt"

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import constants

from myData import (
    read_exoplanetA,
    molar_mass,
    molecules_names,
    column_names,
    read_num_densities
)

data = read_exoplanetA()  # DO NOT REMOVE


# *************************************************************************************

def mass_density(name=None):
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
        return pd.Series(mass_density(read_num_densities()[name], molar_mass[name]), name=name)
    else:
        return pd.concat([mass_density(read_num_densities()[name], molar_mass[name])
                          for name in molecules_names], axis=1)


def effective_mm_q(q):
    '''
    Function to calculate the effective molar mass from the specific humidity.

    Parameter:
        q (float) - specific humidity.

    Returns:
        float
    '''
    return molar_mass['dry_air']/(1 + 0.61*q)


def effective_mm_ep(e, p):
    '''
    Function to calculate the effective molar mass from the 
    water vapour pressure and air pressure.

    Parameters:
        e (float): water vapour pressure.
        p (float): air pressure.

    Returns:
        float
    '''
    md, mv = molar_mass['dry_air'], molar_mass['H2O']
    return md*(1 + (e/p)*((mv/md)-1))


def specific_humidity():
    '''
    Function to calculate the specific humidity.
    Returns pd Series.
    '''
    water_vapour_density = mass_density('H2O')
    return pd.Series(water_vapour_density/data.air_density, name="specific_humidity")


def mass_fraction(name=None):
    '''
    Parameter:
        name (str): Optional, name of compound.

    Returns:
        if name parameter is given -> Series.
        otherwise -> DataFrame.
    '''

    if name:
        return pd.Series(mass_density(name)/data.air_density, name=name)
    else:
        mass_density = mass_density()
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
    sigma = 0.0720  # water surface tension.
    return Clau_Clap_eqn(T)*np.exp((2*18e-3*sigma)/(r*1e3*constants.gas_constant*T))


# *************************************************************************************


def plot_vs_pressure(x, title=None, xlabel=None, label=None, kind=None):
    '''
    Function to make plots againist pressure

    '''
    p = read_exoplanetA().pressure/100

    if kind:
        if kind == "semilogx":
            plt.semilogx(x, p, label=label)
        elif kind == "semilogy":
            plt.semilogy(x, p, label=label)
        elif kind == "loglog":
            plt.loglog(x, p, label=label)
    else:
        plt.plot(x, p, label=label)

    plt.gca().invert_yaxis()
    plt.title(title, fontsize=14)
    plt.ylabel("Pressure $[hPa]$")
    plt.xlabel(xlabel)
    plt.grid()
