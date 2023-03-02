
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
    density = number_density * molar_mass

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
    m = m_d / (1 + 0.61q)

    Parameter:
        q (float) - specific humidity.

    Returns:
        float
    '''
    return molar_mass['dry_air']/(1 + 0.61*q)


def effective_mm_ep(e, p):
    '''
    Function to calculate the effective molar mass from the water vapour pressure and air pressure.
    m = md / {1 + (e/p)(mv/md)-1)}

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
    q = water_vapour_density / total_density 

    Returns pd Series.
    '''

    water_vapour_density = mass_den('H2O')
    return pd.Series(water_vapour_density/data.air_density, name="specific_humidity")


def mass_frac(name=None):
    '''
    Function to calculate the mass fraction of a compound.
    x = mass_density / total density

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


def potential_temperature(T, p, c_p=None, p_r=None):
    '''
    Function to calculate the potential temperature
    T = T_0 * (p_r/p)^k

    Parameters
        T (float, array_like): temperature.
        p (float, array_like): pressure.
        c_p (float, array_like): specific heat capacity at constant pressure.
        p_r (float): reference pressure, optional.

    Returns
        temperature as float/array_like, units are K/Pa.
    '''

    if not p_r:  # if a reference pressure isn't given
        p_r = data.pressure.max() # surface pressure of exoplanet

    k = 2/7
    # if c_p isn't passed
    if type(c_p) == (pd.Series or np.array or list):
        effmm = (data.air_density*constants.gas_constant *
                 data.temperature)/data.pressure  # effective molar mass
        k = (constants.gas_constant/(effmm*c_p))

    return T*(p_r/p)**k




# *************************************************************************************

def get_Unk_mass_den(name="Unk"):
    '''
    Function to return the "unknown" (Helium) mass_density, (from Assignment 1).

    Works by subtracting each mass density from the total density for each iteration.

    Parameters:
     name (str): name given to pandas series, default "Unk"

    '''
    mass_density = mass_den()
    return pd.Series(data.air_density - mass_density.sum(axis=1), name='Unk')


def get_Unk_mm(name="Unk"):
    '''
    Function to return the "unknown" (Helium) molar mass, (from Assignment 1).

    Works by reversing the effective molar mass equation.

    Parameters:
     name (str): name given to pandas series, default "Unk"

    '''
    mass_density = mass_den()
    mass_fractions = mass_frac()
    x_mass_density = get_Unk_mass_den()
    mass_density = pd.concat([mass_density, x_mass_density], axis=1)

    effmm = (data.air_density*constants.gas_constant*data.temperature)/data.pressure
    ratios = pd.concat([mass_fractions[col]/molar_mass[col] for col in molecules_names], axis=1)
    x_molar_mass =  ((1/effmm) - ratios.sum(axis=1)).pow(-1) * (mass_density.Unk/data.air_density)

    return pd.Series(x_molar_mass, name=name)


def get_Unk_mf(name='Unk'):
    '''
    Function to return the "unknown" (Helium) mass fraction, (from Assignment 1).

    mass_density_Unk / total density
    
    Parameters:
     name (str): name given to pandas series, default "Unk"

    '''
    return pd.Series((get_Unk_mass_den()/data.air_density), name="Unk")