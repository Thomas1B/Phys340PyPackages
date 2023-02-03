import numpy as np
import pandas as pd

from .main import molar_mass


def effective_mm_q(q):
    '''
    Function to calculate the effective molar mass from the specific humidity.
    
    Parameter:
        q (float) - specific humidity.

    Returns:
        float
    '''
    return  molar_mass['dry_air']/(1 + 0.61*q)


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