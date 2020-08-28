import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import re
import subprocess
import json
import pandas as pd
import numpy as np

## grabbing the ingredients from bbc food

def get_ingredients_url(url):

    page = requests.get(f'{url}')
    soup = BeautifulSoup(page.content, 'html.parser')
    ingredient = []

    for a in soup.find_all('li', class_ = "recipe-ingredients__list-item"):
        ingredient.append(a.get_text())


    return ingredient

def url_to_df(url):

    recipe = get_ingredients_url(url)

    our_punctuation = '!"#$%&\'())*+-:;<=>?@[\\]^_`{|}~'

    my_list = []

    names = []
    units = []
    qtys = []

    for ingredient in recipe:

        for punctuation in our_punctuation:
        # cleaning for common issues
            ingredient = ingredient.replace(punctuation, '')

        ingredient = ingredient.replace('can', '')
        ingredient = ingredient.replace('package', '')
        ingredient = ingredient.replace('container', '')
        ingredient = ingredient.replace('eggs eggs', 'eggs')
        ingredient = ingredient.replace('⅓', '.33')
        ingredient = ingredient.replace('½', '.5')
        ingredient = ingredient.replace('¼', '.25')
        ingredient = ingredient.replace('¾', '.75')
        ingredient = ingredient.replace('tsp', 'teaspoon')
        ingredient = ingredient.replace('tbsp', 'tablespoon')

        #ingredient = re.sub("^.*\(", "", ingredient)
        try:
            ingredient = re.match("^(.+?),", ingredient).group(0)
        except:
            pass

    #running in the model

        parsed_ingredient = subprocess.check_output(f"echo {ingredient} | ../parsing_tools/parse-ingredients.py --model-file ../parsing_tools/20200825_0846-nyt-ingredients-snapshot-2015-461547e.crfmodel", shell=True)
        parsed_ingredient = json.loads(parsed_ingredient)


    #appending to separate lists taking into account edge cases
        if 'name' in parsed_ingredient[0].keys():

            tmp = parsed_ingredient[0]['name']
            useless_quantifiers = ['oz', 'fl', 'ounce']

            try:
                names.append(re.search("[^\d]*$", tmp).group(0))
            except:
                names.append(tmp)


            #else:
            #    names.append(tmp)
        else:
            names.append(np.nan)

        if 'gram' in parsed_ingredient[0]['input']:
            units.append('gram')
        elif 'milliliters' in parsed_ingredient[0]['input']:
            units.append('ml')
        elif 'unit' in parsed_ingredient[0].keys():
            units.append(parsed_ingredient[0]['unit'])
        else:
            units.append('unit')


        if 'qty' in parsed_ingredient[0].keys():
            qtys.append(parsed_ingredient[0]['qty'])
        else:
            try:
                qtys.append(float(parsed_ingredient[0]['input'][:3]))
            except:
                qtys.append(np.nan)


    final_df = pd.DataFrame(list(zip(qtys, units, names)), columns = ['qty', 'unit', 'name'])
    final_df = final_df[final_df['name'].notna()]
    final_df = final_df[final_df['unit'].notna()]
    final_df = final_df[final_df['unit'] != 'teaspoon']

    return final_df


