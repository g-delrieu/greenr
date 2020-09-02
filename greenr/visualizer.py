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
    labels = ["{0} ({1}%)".format(k, (round(100 * v/sum([v for k,v in data.items()])))) for k, v in data.items()]

    labelswrapped = [ '\n'.join(wrap(l, 30)) for l in labels]

    # Git gud colors
    num_colors = len(labels)
    cm = pylab.get_cmap('brg')
    clist = [cm(1.*i/num_colors) for i in range(num_colors)]

    totalghg = sum([v for k,v in data.items()])

    iconsize = totalghg * 40 / 13.6

    # Plot
    fig = plt.figure(
        FigureClass=Waffle,
        figsize=(12,6),
        rows=5,
        values=values,
        #cmap_name="tab20b",
        colors=clist,
        labels=labelswrapped,
        icons='car-side',
        icon_size=iconsize,
        icon_legend=True,
        vertical = False,
        legend={'loc': 'lower center', 'bbox_to_anchor': (0.5, -.5),'ncol': 3, 'fontsize': 14},
        title = {
        'label': 'Impact breakdown: Each car represents\ndriving 1 kilometer with a petrol car',
        'loc': 'left',
        'pad': 10,
        'fontdict': {
            'fontsize': 30
        }
        }
    )

    fig.gca().set_facecolor('#EEEEEE')
    fig.set_facecolor('#EEEEEE')

    return plt.show(), x

def hbarchart(df_parsed):

    x = df_parsed.groupby('raw_ingredient')['impact'].sum()

    # Define car row
    car = pd.Series({'Driving a petrol car for 1 kilometers': .25}, name = 'impact')
    x = x.append(car)

    # Replace small ingredients by 'Other'
    x = x.reset_index()
    x.loc[x['impact'] < 0.2, 'index'] = 'Other'
    x = x.groupby('index')['impact'].sum()
    x.sort_values(ascending=False, inplace=True)

    ''' # Give specific color to car row
             colors = []
             for ingredient in x.index: # keys are the names of the boys
                 if ingredient == 'Driving a petrol car for 10 kilometers':
                     colors.append('#808080')
                 else:
                     colors.append('#86bf91')
         '''


    # Start plotting
    fig, ax = plt.subplots()

    '''bin_width = np.diff(x.values)

                y = x.values'''

    barx = [0] + list(x.values)
    y = [100 * el / sum(list(x.values)) for el in list(x.values)]
    bin_width = list(x.values)

    bar_plot = ax.bar(
        x = np.cumsum(barx[:-1]),
        height = y,
        width=bin_width,
        align='edge',
        edgecolor='white'
        )

    debugvalue = barx

    # Setting appropriate axis limits
    ax.set_xlim(0, sum(x.values)/.9)
    ax.set_ylim(0,100)

    # Set title
    ax.set_title('Breakdown of recipe CO2 impact (kg, %)', pad = 30, loc = 'left')

    # Despine
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    #ax.spines['left'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)

    # Switch off ticks
    #ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

    # Draw vertical axis lines
    #vals = ax.get_xticks()
    #for tick in vals:
    #  ax.axvline(x=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

    # Set x-axis label
    ax.set_xlabel("Ingredient CO2 impact (kg)", labelpad=20, weight='bold', size=12)

    # Set y-axis label
    ax.set_ylabel("Relative ingredient impact \n (% of recipe total)", labelpad=20, weight='bold', size=12)

    # Format y-axis label
    #ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))

    # Wrap y-axis labels
    #labels = x.index.values
    #labels = [ '\n'.join(wrap(l, 30)) for l in labels ]
    #ax.set_xticklabels(labels)

    return plt.show(), debugvalue

