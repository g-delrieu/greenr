import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.gridspec import GridSpec

import matplotlib.pyplot as plt

def piechart(df_parsed):

    df_parsed['raw_ingredient']
    df_parsed.sort_values(['impact'], ascending=False, inplace=True)
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:

    labels = df_parsed['raw_ingredient']
    sizes = df_parsed['impact']
    #explode = [0.1] + [0] * (len(labels) - 1)  # Explode the first part of the pie

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return plt.show()

