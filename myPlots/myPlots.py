import matplotlib.pyplot as plt
from myData import read_exoplanetA




def plot_vs_pressure(x, title=None, xlabel=None, label=None, kind=None):
    '''
    Function to make plots againist pressure

    Parameters:
        x (array_like): values to be plotted on the x-axis.
        title (str): title of plot.
        xlabel (str): x-axis label.
        label (list_like): labels for legend.
        kind (logx, logy, loglog): which kind of plot to use, default linear.
    
    '''
    p = read_exoplanetA().pressure/100

    if kind:
        if kind == "logx": plt.semilogx(x, p, label=label)
        elif kind == "logy": plt.semilogy(x, p, label=label)
        elif kind == "loglog": plt.loglog(x, p, label=label)
    else:
        plt.plot(x, p, label=label)

    plt.gca().invert_yaxis()
    plt.title(title, fontsize=14)
    plt.ylabel("Pressure $[hPa]$")
    plt.xlabel(xlabel)
    plt.grid()