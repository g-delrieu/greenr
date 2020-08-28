import pandas as pd

import scraper_parser
import matching
import calculator

def calculate(url):

    df_parsed = scraper_parser.url_to_df(url)


    categories = matching.get_categories(df_parsed, try_google = True)

    df_parsed['name'] = categories

    ghg_impact = calculator.ghg_calc(df_parsed)

    return ghg_impact
