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

def waffleplot(out, rec, en = True):

    df_parsed = out[1]
    servingsize = out[2]
    recipe_title = out[3]

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
    x['impact'] = x['impact']/float(servingsize)
    total = x['impact'].sum()
    x['CO2 per Ingredient:'] = x['Ingredients'] + ': ' + (round(x['impact']/total*100)).astype(int).astype(str) + "%"
    x['source'] = recipe_title
    x = x.append(pd.DataFrame([['All',rec['impact'],rec['title'] + ': 100%',rec['title']]], columns = x.columns)).reset_index(drop = True)

    # Turn df into dict for graph
    data = {x['CO2 per Ingredient:'][i]: x['impact'][i] for i in range(len(x['impact']-1))}

    # Define labels for legend, wrap at 25 characters
    labels = ["{0} ({1}%)".format(k, round(100 * v/sum([v for k,v in data.items()]))) for k, v in data.items()]
    labelswrapped = [ '\n'.join(wrap(l, 40)) for l in labels]

    print(x)

    selection = alt.selection_multi(fields=['CO2 per Ingredient:'], bind='legend')
    chart1 = alt.Chart(x[:-1]).mark_bar(size = 100).encode(
    alt.Y('sum(impact)', scale=alt.Scale(domain=[0, total]), axis = None),

    color = alt.Color('CO2 per Ingredient:', scale=alt.Scale(scheme='spectral', domain = list(x['CO2 per Ingredient:'])[:-1])),
    order = alt.Order('impact:N', sort='descending'),
    opacity = alt.condition(selection, alt.value(1), alt.value(0.2))).add_selection(selection).properties(width = 250,
                                                                                                          height = 350,
                                                                                                          title = {"text": x['source'][0],
                                                                                                                   "color": "white",
                                                                                                                   "fontSize": 20})


    chart2 = alt.Chart(x.iloc[[-1]]).mark_bar(size = 100, color = "orange").encode(
    alt.Y('sum(impact)', scale=alt.Scale(domain=[0, total]), axis = None),
    color = alt.Color('CO2 per Ingredient::N', scale=alt.Scale(scheme='rainbow')),
    opacity = alt.condition(selection, alt.value(1), alt.value(0.2))).properties(width = 250,
                                                                                 height = 350,
                                                                                 title = {"text": x['source'].iloc[-1],
                                                                                          "color": "white",
                                                                                          "fontSize": 20})

    chart = alt.hconcat(chart1, chart2).configure(background = '#466d1d').configure_view(strokeOpacity=0).resolve_scale(
    color='independent')

    chart = chart.configure_legend(padding=30,
                           orient='bottom',
                           direction = 'vertical',
                           offset = 0,
                           labelColor = 'white',
                           titleColor = 'white',
                           titleFont = "IBM Plex Mono",
                           titleFontSize = 20,
                           titleFontWeight = 'bold',
                           titleLimit = 0,
                           labelFontSize = 15,
                           labelLimit= 0)



    return chart
