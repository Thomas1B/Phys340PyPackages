import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import constants

main_path = '../../Data/'

from ..main import (
    molecules_names,
    column_names,
    molar_mass
)


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