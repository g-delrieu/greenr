import pandas as pd
import re

data = pd.read_csv('data/Final_conversion_table.csv')

data = data.drop(['Average tablespoon (grams)', 'Source', 'Average Unit (if applicable) (grams)', 'Source.1'], axis = 1)
data.columns = ['name','tablespoon','unit','ghg']
data = data.set_index('name')

def ghg_calc(df):
    impact = []
    df = df.reset_index()
    for i in range(len(df.unit)):


        if str(df.qty[i]).replace(".", "", 1).isdigit() and df.name[i] != 'No match found':
            if df.unit[i] == 'tablespoon':
                impact.append(float(df.qty[i])*float(data.tablespoon[df.name[i]])*float(data.ghg[df.name[i]]))
            elif df.unit[i] == 'unit':
                impact.append(float(df.qty[i])*float(data.unit[df.name[i]])*float(data.ghg[df.name[i]]))
            elif df.unit[i] == 'gram':
                impact.append((float(df.qty[i])/1000)*float(data.ghg[df.name[i]]))
            elif df.unit[i] == 'milliliter':
                impact.append((float(df.qty[i])/1000*float(data.ghg[df.name[i]])))
            elif df.unit[i] == 'kilogram':
                impact.append(float(df.qty[i])*float(data.ghg[df.name[i]]))
            elif df.unit[i] == 'liter':
                impact.append(float(df.qty[i])*float(data.ghg[df.name[i]]))
            else:
                impact.append(0)
        else:
            impact.append(0)
        #import pdb; pdb.set_trace()
    return sum(impact)
