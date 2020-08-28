import pandas as pd

data = pd.read_csv('data/Final_conversion_table.csv')

data = data.drop(['Average tablespoon (grams)', 'Source', 'Average Unit (if applicable) (grams)', 'Source.1'], axis = 1)
data.columns = ['name','tablespoon','unit','ghg']
data = data.set_index('name')

def ghg_calc(df):
    impact = []
    for i in range(len(df.unit)):
        if df.unit[i] == 'tablespoon':
            impact.append(df.qty[i]*data.tablespoon[df.name[i]]*data.ghg[df.name[i]])
        elif df.unit[i] == 'unit':
            impact.append(df.qty[i]*data.unit[df.name[i]]*data.ghg[df.name[i]])
        elif df.unit[i] == 'gram':
            impact.append((df.qty[i]/1000)*data.unit[df.name[i]]*data.ghg[df.name[i]])
        elif df.unit[i] == 'milliliter':
            impact.append((df.qty[i]/1000)*data.unit[df.name[i]]*data.ghg[df.name[i]])
        elif df.unit[i] == 'kilogram':
            impact.append(df.qty[i]*data.ghg[df.name[i]])
        elif df.unit[i] == 'liter':
            impact.append(df.qty[i]*data.ghg[df.name[i]])
        else:
            impact.append(0)

    return sum(impact)
