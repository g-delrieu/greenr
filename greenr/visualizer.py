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

def waffleplot(df_parsed, en = True):

    df_parsed.name = [item.strip('oz').strip()[0].upper()+item.strip('oz').strip()[1:] for item in df_parsed['name']]
    #print(df_parsed.name)
    # Define x(dict)
    x = df_parsed.groupby('name')['impact'].sum()
    x = x.reset_index()

    totalghg = x['impact'].sum()

    # Grouping into "Other"
    if (x['impact'] >= 0.243/2).sum() != x['impact'].size: # Any ingredient smaller than 2.43
        while x[x['name'] == 'Other']['impact'].sum() < 0.243/2 or (x['impact'] >= 0.243/2).sum() != x['impact'].size:
            x.loc[:,'name'].iat[x[x['name'] != 'Other']['impact'].idxmin()] = 'Other'    #turn smallest ingredients name to "Other"
            x = x.groupby('name')['impact'].sum()
            x.sort_values(ascending=False, inplace=True)
            x = x.reset_index()

    # Set 'Other' to bottom of list
    m = x['name'] != 'Other'
    x[m].append(x[~m]).reset_index(drop = True)

    # Turn df into dict for graph
    data = {x['name'][i]: x['impact'][i] for i in range(len(x['impact']))}

    # Define labels for legend, wrap at 25 characters
    labels = ["{0} ({1}%)".format(k, round(100 * v/sum([v for k,v in data.items()]))) for k, v in data.items()]
    labelswrapped = [ '\n'.join(wrap(l, 40)) for l in labels]

    # Define colors
    num_colors = len(labels)
    cm = pylab.get_cmap('Spectral')
    clist = [cm(1.*i/num_colors) for i in range(num_colors)]

    # Define values and title
    #all_val = sum(data.values())
    values = [round(data, 2) for data in data.values()]
    barWidth = 1
    plt.figure(dpi=1200)
    fig = plt.figure(
    figsize = (1.5,2))

    plt.axis('off')
    bars = values[0]
    plt.bar(0, values[0], color=clist[0], edgecolor='white', width=barWidth, label = x['name'][0])
    plt.text(0, values[0]/2, values[0], ha="center", va="center", fontsize=5, fontweight="bold")


    bars = values[0]
    for i in range(1,len(values)):
        plt.bar(0, values[i], bottom=bars, color=clist[i], edgecolor='white', width=barWidth, label = x['name'][i])
        plt.text(0, bars+ values[i]/2, values[i], ha="center", va="center", fontsize=5, fontweight="bold")
        bars += values[i]
    plt.legend( fontsize=5, loc = 'lower center', bbox_to_anchor=(-0.7, bars/i-.1))
    fig.gca().set_facecolor('#466d1d')
    fig.set_facecolor('#466d1d')


    return plt.show()
