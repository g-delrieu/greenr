import pandas as pd

import scraper_parser
import matching
import calculator

def calculate(url):

    df_parsed, servingsize = scraper_parser.url_to_df(url)

    categories = matching.get_categories(df_parsed, try_google = True)

    df_parsed['category'] = categories

    ghg_impact_sum, impact_list = calculator.ghg_calc(df_parsed)

    df_parsed['impact'] = impact_list

    return round(ghg_impact_sum/int(servingsize),1), df_parsed
