import pandas as pd
import re

data = pd.read_csv('data/Final_conversion_table.csv')

data = data.drop(['Average tablespoon (grams)', 'Source', 'Average Unit (if applicable) (grams)', 'Source.1'], axis = 1)
data.columns = ['name','tablespoon','unit','wing','breast','drumstick','thigh','chop','fillet','ghg']
data = data.set_index('name')

def ghg_calc(df):
    impact = []
    df = df.reset_index()

    for i in range(len(df.unit)):

        if str(df.qty[i]).replace(".", "", 1).isdigit() and df.category[i] != 'No match found':
            if df.unit[i] == 'tablespoon':
                impact.append(float(df.qty[i])*float(data.tablespoon[df.category[i]])*float(data.ghg[df.category[i]]))
            elif df.unit[i] == 'unit':
                impact.append(float(df.qty[i])*float(data.unit[df.category[i]])*float(data.ghg[df.category[i]]))
            elif df.unit[i] == 'wing':
                impact.append(float(df.qty[i])*float(data.wing[df.category[i]])*float(data.ghg[df.category[i]]))
            elif df.unit[i] == 'breast':
                impact.append(float(df.qty[i])*float(data.breast[df.category[i]])*float(data.ghg[df.category[i]]))
            elif df.unit[i] == 'drumstick':
                impact.append(float(df.qty[i])*float(data.drumstick[df.category[i]])*float(data.ghg[df.category[i]]))
            elif df.unit[i] == 'thigh':
                impact.append(float(df.qty[i])*float(data.thigh[df.category[i]])*float(data.ghg[df.category[i]]))
            elif df.unit[i] == 'chop':
                impact.append(float(df.qty[i])*float(data.chop[df.category[i]])*float(data.ghg[df.category[i]]))
            elif df.unit[i] == 'fillet':
                impact.append(float(df.qty[i])*float(data.unit[df.category[i]])*float(data.ghg[df.category[i]]))
            elif df.unit[i] == 'gram':
                impact.append((float(df.qty[i])/1000)*float(data.ghg[df.category[i]]))
            elif df.unit[i] == 'milliliter':
                impact.append((float(df.qty[i])/1000*float(data.ghg[df.category[i]])))
            elif df.unit[i] == 'kilogram':
                impact.append(float(df.qty[i])*float(data.ghg[df.category[i]]))
            elif df.unit[i] == 'liter':
                impact.append(float(df.qty[i])*float(data.ghg[df.category[i]]))
            else:
                impact.append(0)
        else:
            impact.append(0)

    impact = [x if str(x) != 'nan' else 0 for x in impact]

    return sum(impact), impact



