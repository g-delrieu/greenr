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
        out = (round(ghg_impact_sum/int(servingsize),1), df_parsed, recipe_title, True)
    else:
        out = (round(ghg_impact_sum,1), df_parsed, False)

    return out
