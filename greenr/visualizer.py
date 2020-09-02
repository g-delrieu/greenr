import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from textwrap import wrap

from pywaffle import Waffle

import pylab

def waffleplot(df_parsed):

    # Define x(dict)
    x = df_parsed.groupby('raw_ingredient')['impact'].sum()
    x = x.reset_index()

    x.loc[x['impact'] < 0.2, 'raw_ingredient'] = 'Other'

    x = x.groupby('raw_ingredient')['impact'].sum()
    x.sort_values(ascending=False, inplace=True)
    x = x.reset_index()
    xdict = {x['raw_ingredient'][i]: x['impact'][i] for i in range(len(x['impact']))}

    data = xdict

    # Define values
    values = [x / 0.243 for x in list(data.values())]

    # Define labels for legend
    labels = ["{0} ({1}%)".format(k, round(100 * v/sum([v for k,v in data.items()]))) for k, v in data.items()]

    labelswrapped = [ '\n'.join(wrap(l, 30)) for l in labels]

    # Define colors
    if len(labels) < 9:
        clist = [
        '#443742',
        '#CEA07E',
        '#EDD9A3',
        '#EDE8C0',
        '#51A3A3',
        '#53A2BE',
        '#89B0AE',
        '#40798C',
        '#628395'
        ][:len(labels)]
    else:
        num_colors = len(labels)
        cm = pylab.get_cmap('Spectral_r')
        clist = [cm(1.*i/num_colors) for i in range(num_colors)]

    totalghg = sum([v for k,v in data.items()])

    iconsize = 60

    # Plot
    fig = plt.figure(
        FigureClass=Waffle,
        figsize = (40,8),
        columns=10,
        values=values,
        colors=clist,
        labels=labelswrapped,
        icons='car-side',
        icon_size=iconsize,
        icon_legend=True,
        vertical = False,
        legend={
        'loc': 'upper left',
        'bbox_to_anchor': (0, -.1),
        'ncol': 3,
        'fontsize': 16,
        'facecolor': '#466d1d',
        'edgecolor': 'white',
        'labelcolor': 'white'
        },
        title = {
        'label': 'Impact breakdown: Each car represents driving 1 kilometer with a petrol car',
        'loc': 'left',
        'pad': 10,
        'color': 'white',
        'style': 'italic',
        'fontdict': {
            'fontsize': 30
        }
        }
    )

    fig.gca().set_facecolor('#466d1d')
    fig.set_facecolor('#466d1d')

    return plt.show(), x
