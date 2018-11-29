from . import pyUtils as py
from . import figureUtilsVenn as pyvenn

np      = py.loadExternalModule('numpy')
plt     = py.loadExternalModule('matplotlib.pylab')
pltvenn = py.loadExternalModule('matplotlib_venn')

###############################################################################

def subplots(flatten=True, dpi=300, **kwargs):
    """
    Wrapper for matplotlib subplots

    Inputs:
      - flatten : Flatten the list of axes, if 2D.
      - dpi : DPI of figure
      - **kwargs : Arguments to subplots
    Output:
     - fig : matplotlib figure
     - axes : array of matplotlib axes

    Typical usage:
     fig, axes = subplots(nrows=2, ncols=2)
    """

    fig, axes = plt.subplots(dpi=dpi, **kwargs)
    if hasattr(axes, '__len__') and flatten:
        axes = axes.flatten()
    else:
        axes = [axes]
    #fi
    return fig, axes
#edef

###############################################################################

def venn(*sets, ax=None, names=None):
    """
    Draw a venn diagram for between 2-6 sets
    Inputs:
      - *sets: sets to consider
      - ax : Axis to draw on (only works for 2-3 venn groups
      - names : Names of sets
    Outputs:
      - fig : Matplotlib figure
      - ax : Matplotlib axis
    """

    nsets = len(sets)
    if nsets == 2:
        return pltvenn.venn2(sets, ax=ax, set_labels=names)
    elif nsets == 3:
        return pltvenn.venn3(sets, ax=ax, set_labels=names)
    elif (nsets >= 4) & (nsets <= 6):
        labels = pyvenn.get_labels(sets, fill=['number', 'logic'])
        fig, ax = { 4: pyvenn.venn4, 5: pyvenn.venn5, 6: pyvenn.venn6}[nsets](labels, names=names)
        fig.show()
        return fig, ax
    else:
        raise NotImplementedError
    #fi
#edef

###############################################################################

def equal_xlim_ylim(axes, xlim=None, ylim=None):
    """
    For a set of axes, make all xlimits and ylimits the same.
    Inputs:
        axes: A list of matplotlib axes
        xlim: Tuple of (min, max) limits for x-axis. or None, (then it is taken from the ranges already in the axis)
        ylim: Tuple of (min, max) limits for y-axis. or None, (then it is taken from the ranges already in the axis)
    Outputs:
        A tuple:
        ( (min_x, max_x), (min_y, max_y) )
    """
    if xlim is None:
        xlim = [ f(list(zip(*[ ax.get_xlim() for ax in axes ]))) for f in [ np.min, np.max ] ]
    #fi
    [ ax.set_xlim(xlim) for ax in axes ]
    
    if ylim is None:
        ylim = [ f(list(zip(*[ ax.get_ylim() for ax in axes ]))) for f in [ np.min, np.max ] ]
    #fi
    [ ax.set_ylim(ylim) for ax in axes ]
    
    return (xlim, ylim)
#edef