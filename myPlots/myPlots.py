import matplotlib.pyplot as plt
from ..myData import read_exoplanetA
import numpy as np
import pandas as pd




def plot_vs_pressure(x, title=None, xlabel=None, label=None, kind=None, slice=False):
    
    '''
    Function to make plots againist pressure

    Parameters:
        x (array_like): values to be plotted on the x-axis.
        title (str): title of plot.
        xlabel (str): x-axis label.
        label (list_like): labels for legend.
        kind (logx, logy, loglog): which kind of plot to use, default linear.
        slice: (bool): True -> auto slices y-data to fit x-data. 
    
    '''

    p = read_exoplanetA().pressure/100
    if slice: 
        p = p.iloc[:len(xx)]    

    def plot(xx):

        if kind:
            if kind == "logx" or 'semilogx' or 'logX': plt.semilogx(xx, p, label=label)
            elif kind == "logy" or 'semilogy' or 'logY': plt.semilogy(xx, p, label=label)
            elif kind == "loglog" or 'log' or 'Log': plt.loglog(xx, p, label=label)
        else:
            plt.plot(xx, p, label=label)

    print(type(x[0]))

    if type(x) == (list or np.array or pd.Series):
        for arr in x:
            plot(arr)
    else:
        plot(x)

    plt.gca().invert_yaxis()
    plt.title(title, fontsize=14)
    plt.ylabel("Pressure $[hPa]$", fontsize=12)
    plt.xlabel(xlabel, fontsize=12)
    plt.grid()




def save_plot(name, path= "WriteUp/Figures/", dpi=500, filetype='.jpeg'):
    '''
    Function to save a plot,

    Parameters:
        name (str): name to plot be saved as.
        path (str): filepath to desired location. (default: WriteUp/Figures/)
        dpi (int): image quaility (optional).
        filetype (str): filetype to be saved as.
    '''
    full_path = path + name + filetype
    plt.savefig(full_path, dpi=dpi)