import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from textwrap import wrap

def hbarchart(df_parsed):

    #df_parsed.sort_values(['impact'], ascending=False, inplace=True)

    x = df_parsed.groupby('raw_ingredient')['impact'].sum()

    # Define car row
    car = pd.Series({'Driving a petrol car for 10 kilometers': 2.5}, name = 'impact')
    x = x.append(car)
    x = x.reset_index()

    x.loc[x['impact'] < 0.2, 'index'] = 'Other'
    x = x.groupby('index')['impact'].sum()
    x.sort_values(ascending=False, inplace=True)

    # Give specific color to car row
    colors = []
    for ingredient in x.index: # keys are the names of the boys
        if ingredient == 'Driving a petrol car for 10 kilometers':
            colors.append('#808080')
        else:
            colors.append('#86bf91')

    debugvalue = x.values

    # Start plotting
    fig, ax = plt.subplots()

    ax.bar(
        x = list(range(len(x))),
        height = x.values,
        color=colors,
        width= x.values
        )

    # Set title
    ax.set_title('Breakdown of recipe CO2 impact (kg, %)')

    # Despine
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Switch off ticks
    ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

    # Draw vertical axis lines
    vals = ax.get_xticks()
    for tick in vals:
      ax.axvline(x=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

    # Set x-axis label
    ax.set_xlabel("Ingredient", labelpad=20, weight='bold', size=12)

    # Set y-axis label
    ax.set_ylabel("CO2 impact", labelpad=20, weight='bold', size=12)

    # Format y-axis label
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))

    # Wrap y-axis labels
    labels = x.index.values
    labels = [ '\n'.join(wrap(l, 30)) for l in labels ]
    ax.set_xticklabels(labels)

    return plt.show(), debugvalue

