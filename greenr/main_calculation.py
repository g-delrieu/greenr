import os


print('===== printing directory =======')
os.system('pwd')

print('===== printing content directory =======')
os.system('ls')

import pandas as pd

import scraper_parser
import matching
import calculator
from urllib.parse import urlparse
import pymongo

# Establishing DB connection
mongo_key = os.environ.get('DB_PASSWORD')

myclient = pymongo.MongoClient(f"mongodb+srv://gdelrieu:{mongo_key.strip()}@cluster0.jceas.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["greenr"]



def updating_database_bbc(out):
    mycol = mydb["recorded_recipes"]

    ## checking if recipe already recorded and adding it if not

    if mycol.find({"url":out[3]}).count() == 0:

        mydict = {"impact": out[0], "title": out[3], "url": out[4]}

        mycol.insert_one(mydict)

    return None




def calculate(url):

    o = urlparse(url)
    en = False


    if o.netloc == 'www.bbc.co.uk':
        try:
            en = True
            df_parsed, servingsize, raw_ingredient_list, recipe_title = scraper_parser.url_to_df(url)
        except:
            print('invalid input')

    elif o.netloc == 'www.marmiton.org':
        try:
            df_parsed = scraper_parser.marmiton_to_df(url)
        except:
            print('invalid input')
    else:
        print('invalid input')


    categories = matching.get_categories(df_parsed, try_google = True)

    df_parsed['category'] = categories


    ghg_impact_sum, impact_list = calculator.ghg_calc(df_parsed)

    df_parsed['impact'] = impact_list

    if en:
        df_parsed['raw_ingredient'] = raw_ingredient_list[:-1]
        out = (round(ghg_impact_sum/int(servingsize),1), df_parsed, servingsize, recipe_title, url, True)
        updating_database_bbc(out)
    else:
        out = (round(ghg_impact_sum,1), df_parsed, servingsize, url, False)

    return out




def finding_better_recipe(out):
# comparing impact of recipe with recorded recipes and fetching better recipe if it exist
    mycol = mydb['recorded_recipes']

    current_impact = out[0]

    match = mycol.find_one({"impact":{'$lt':current_impact}})

    return match
