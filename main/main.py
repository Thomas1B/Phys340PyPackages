
# This module is specific to one dataset "exoplanet_2023A_data.txt"

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import constants

from ..myData import (
    read_exoplanetA,
    molar_mass,
    molecules_names,
    column_names,
    read_num_densities
)

data = read_exoplanetA()  # DO NOT REMOVE


# *************************************************************************************

def mass_den(name=None):
    '''
    Function to calculate the mass density from the number density and molar mass of a given element/compound.

    Parameter:
        name (str): Optional, name of compound.

    Returns:
        if name parameter is given -> Series.
        otherwise -> DataFrame.
    '''

    def mass_d(num_density, molar_mass):
        return (num_density*molar_mass)/constants.Avogadro

    if name:
        return pd.Series(mass_d(read_num_densities()[name], molar_mass[name]), name=name)
    else:
        return pd.concat([mass_d(read_num_densities()[name], molar_mass[name])
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


def spec_humidity():
    '''
    Function to calculate the specific humidity.

    Returns pd Series.
    '''
    
    water_vapour_density = mass_den('H2O')
    return pd.Series(water_vapour_density/data.air_density, name="specific_humidity")


def mass_frac(name=None):
    '''
    Function to calculate the mass fraction of a compound.

    Parameter:
        name (str): Optional, name of compound.

    Returns:
        if name parameter is given -> Series.
        otherwise -> DataFrame of all compounds.
    '''

    if name:
        return pd.Series(mass_den(name)/data.air_density, name=name)
    else:
        mass_density = mass_den()
        mass_fraction = pd.concat([mass_density[name]/data.air_density
                                   for name in mass_density], axis=1)
        mass_fraction.columns = mass_density.columns
        return mass_fraction


def clau_clap_eqn(T, L=2.45e6):
    '''
    Function to calculate the saturation vapour pressure over a flat surface
    using the Clausius-Clapeyron equation.

    Parameters:
        T (float): temperature in kelvin.
        L (optional): Specific enthalpy, default -> vapourization.

    Returns:
        pressure in hPa.
    '''
    k = (molar_mass['wet_air']*L)/constants.gas_constant
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
    k = constants.gas_constant/(molar_mass['wet_air']*L)
    return 1/(273**-1 - k*np.log(e/e0))


def kelvin_eqn(r, T):
    '''
    Function to calculate the saturation vapour pressure for a droplet of radius using the kelvin equation.

    Parameters:
        r (float) radius of droplet, pass in meters!.
        T (float) temperature
    '''
    sigma = 0.0720  # [N/m] coefficient of water surface tension.
    return clau_clap_eqn(T)*np.exp((2*molar_mass['wet_air']*sigma)/(r*1e3*constants.gas_constant*T))

def potential_temperature(T, p, p_r=700e2):
    '''
    Function to calculate the potential temperature

    Parameters
        T (float, array_like): temperature.
        p (float, array_like): pressure.
        p_r (float): reference pressure.

    Returns
        temperature as float/array_like, units are K/Pa.
    '''
    return T*(p_r/p)**(2/7)