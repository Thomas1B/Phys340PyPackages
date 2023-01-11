import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import constants

molecules_names = ['N2', 'CO', 'O2', 'H2', 'Ar', 'H2O']

data_path = "../../Data/exoplanet_2023A_data.txt"
column_names = ['pressure', 'temperature', 'air_density', 'zonal_wind', 'merid_wind', 'N2', 'CO', 'O2', 'H2', 'Ar', 'H2O']
data = pd.read_csv(data_path, sep='\s+', skiprows=13, names=column_names)
data[molecules_names] *= 1e22 # getting full number, see data file for explaination.
number_densities = pd.concat([data[name] for name in molecules_names], axis=1)


atomic_mass = {
    # molar mass, in  Kg/mol 
    "N2" : 28.013e-3,
    'CO' : 28.010e-3,
    'O2' : 15.999e-3,
    'H2' : 2.016e-3,
    'Ar' : 39.948e-3,
    'H2O' : 18.015e-3
}


def plot_vs_pressure(x, title, xlabel, *args):
    '''
    Function to make plots againist pressure
    '''
    plt.plot(x, data.pressure)
    plt.gca().invert_yaxis()


    plt.title(title, fontsize=14)
    plt.ylabel("Pressure $[Pa]$")
    plt.xlabel(xlabel)    

def calc_mass_density(num_density, molar_mass):
    '''
    Function to calculate the mass density from the number density and molar mass
    of a given element/compound.
    '''
    return (num_density*molar_mass)/constants.Avogadro


# Computing mass densities

N2_density = calc_mass_density(data.N2, atomic_mass['N2'])
CO_density = calc_mass_density(data.CO, atomic_mass['CO'])
O2_density = calc_mass_density(data.O2, atomic_mass['O2'])
H2_density = calc_mass_density(data.H2, atomic_mass['H2'])
Ar_density = calc_mass_density(data.Ar, atomic_mass['H2'])
H2O_density = calc_mass_density(data.H2O, atomic_mass['H2O'])
mass_densities = pd.concat([N2_density, CO_density, O2_density, H2_density, Ar_density, H2O_density], axis=1)