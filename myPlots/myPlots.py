import matplotlib.pyplot as plt
from ..myData import read_exoplanetA




def plot_vs_pressure(x, title=None, xlabel=None, label=None, kind=None, y=False):
    '''
    Function to make plots againist pressure

    Parameters:
        x (array_like): values to be plotted on the x-axis.
        title (str): title of plot.
        xlabel (str): x-axis label.
        label (list_like): labels for legend.
        kind (logx, logy, loglog): which kind of plot to use, default linear.
        y: (bool): True auto slices y-data to fit x-data. 
    
    '''
    p = read_exoplanetA().pressure/100
    if y: 
        p = p.iloc[:len(x)]

    if kind:
        if kind == "logx" or 'semilogx' or 'logX': plt.semilogx(x, p, label=label)
        elif kind == "logy" or 'semilogy' or 'logY': plt.semilogy(x, p, label=label)
        elif kind == "loglog" or 'log' or 'Log': plt.loglog(x, p, label=label)
    else:
        plt.plot(x, p, label=label)

    plt.gca().invert_yaxis()
    plt.title(title, fontsize=14)
    plt.ylabel("Pressure $[hPa]$")
    plt.xlabel(xlabel)
    plt.grid()