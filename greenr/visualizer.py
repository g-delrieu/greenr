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
import altair as alt





def waffleplot(df_parsed, en = True):


    df_parsed = df_parsed.sort_values('impact')
    df_parsed = df_parsed.rename(columns={"name": "Ingredients"})
    df_parsed['Ingredients'] = [item.replace('oz', '').strip()[0].upper()+item.replace('oz', '').strip()[1:] for item in df_parsed['Ingredients']]
    # Define x(dict)
    x = df_parsed.groupby('Ingredients')['impact'].sum()
    x = x.reset_index()

    totalghg = x['impact'].sum()

    # Grouping into "Other"
    if (x['impact'] >= 0.243/2).sum() != x['impact'].size: # Any ingredient smaller than 2.43
        while x[x['Ingredients'] == 'Other']['impact'].sum() < 0.243/2 or (x['impact'] >= 0.243/2).sum() != x['impact'].size:
            x.loc[:,'Ingredients'].iat[x[x['Ingredients'] != 'Other']['impact'].idxmin()] = 'Other'    #turn smallest ingredients name to "Other"
            x = x.groupby('Ingredients')['impact'].sum()
            x.sort_values(ascending=False, inplace=True)
            x = x.reset_index()

    # Set 'Other' to bottom of list
    m = x['Ingredients'] != 'Other'
    x[m].append(x[~m]).reset_index(drop = True)
    total = x['impact'].sum()
    x['CO2 per Ingredient:'] = x['Ingredients'] + ': ' + (round(x['impact']/total*100)).astype(int).astype(str) + "%"
    print(x)

    # Turn df into dict for graph
    data = {x['CO2 per Ingredient:'][i]: x['impact'][i] for i in range(len(x['impact']))}

    # Define labels for legend, wrap at 25 characters
    labels = ["{0} ({1}%)".format(k, round(100 * v/sum([v for k,v in data.items()]))) for k, v in data.items()]
    labelswrapped = [ '\n'.join(wrap(l, 40)) for l in labels]

    selection = alt.selection_multi(fields=['CO2 per Ingredient:'], bind='legend')
    chart = alt.Chart(x).configure(background = '#466d1d' ).mark_bar(size = 100).encode(
    alt.Y('sum(impact)', axis = None),
    color = alt.Color('CO2 per Ingredient:', scale=alt.Scale(scheme='spectral', domain = list(x['CO2 per Ingredient:']))),
    order = alt.Order('impact:N', sort='descending'),
    opacity = alt.condition(selection, alt.value(1), alt.value(0.2))).configure_view(strokeOpacity=0).add_selection(
    selection)

    chart = chart.configure_legend(padding=70,
                           orient='left',
                           labelColor = 'white',
                           titleColor = 'white',
                           titleFont = "IBM Plex Mono",
                           titleFontSize = 20,
                           titleFontWeight = 'bold',
                           titleLimit = 0,
                           labelFontSize = 15,
                           labelLimit= 0)



    return chart
