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

    totalghg = x['impact'].sum()

    # Grouping into "Other"
    if (x['impact'] >= 0.243/2).sum() != x['impact'].size: # Any ingredient smaller than 2.43
        while x[x['raw_ingredient'] == 'Other']['impact'].sum() < 0.243/2 or (x['impact'] >= 0.243/2).sum() != x['impact'].size:
            x.loc[:,'raw_ingredient'].iat[x[x['raw_ingredient'] != 'Other']['impact'].idxmin()] = 'Other'    #turn smallest ingredients name to "Other"
            x = x.groupby('raw_ingredient')['impact'].sum()
            x.sort_values(ascending=False, inplace=True)
            x = x.reset_index()

    # Set 'Other' to bottom of list
    m = x['raw_ingredient'] != 'Other'
    x[m].append(x[~m]).reset_index(drop = True)

    # Turn df into dict for graph
    data = {x['raw_ingredient'][i]: x['impact'][i] for i in range(len(x['impact']))}

    # Define labels for legend, wrap at 25 characters
    labels = ["{0} ({1}%)".format(k, round(100 * v/sum([v for k,v in data.items()]))) for k, v in data.items()]
    labelswrapped = [ '\n'.join(wrap(l, 25)) for l in labels]

    # Define colors
    num_colors = len(labels)
    cm = pylab.get_cmap('RdYlGn')
    clist = [cm(1.*i/num_colors) for i in range(num_colors)]

    # Define values and title
    values = [x / 0.243 for x in list(data.values())]
    title = f'Total recipe: Each car represents driving\n1 kilometer with a petrol car ({round(totalghg/0.243,1)} in total)'

    # Changing car size and row count based on total GHG
    if totalghg/0.243 <= 60:
        iconsize = 40
        row_count = 6
    elif totalghg/(0.243/2):
        iconsize = 20
        row_count = 12
    else:
        iconsize = 10
        row_count = 24

    # Plot
    fig = plt.figure(
        FigureClass=Waffle,
        figsize = (24,8),
        rows=row_count,
        values=values,
        colors=clist,
        labels=labelswrapped,
        #rounding_rule='ceil',
        icons='car-side',
        icon_size=iconsize,
        icon_legend=True,
        vertical = False,
        block_arranging_style='new-line',
        legend={
        'loc': 'upper left',
        'bbox_to_anchor': (0, -.1),
        'ncol': 3,
        'fontsize': 14,
        'facecolor': '#466d1d',
        'edgecolor': 'white',
        'labelcolor': 'white',
        'borderpad': 1
        },
        title = {
        'label': title,
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

    return plt.show()
