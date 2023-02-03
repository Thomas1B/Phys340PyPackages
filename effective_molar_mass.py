import numpy as np
import pandas as pd

def eff_molar_mass_ep(e, p):
    '''
    Function to calculate the effective molar mass from the 
    water vapour pressure and air pressure.

    Parameters:
        e (float): water vapour pressure.
        p (float): air pressure.
    '''
    md, mv = 29, 18
    return md*(1 + (e/p)*((mv/md)-1))