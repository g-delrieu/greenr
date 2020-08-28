import pandas as pd
import app.parser_scraper
import app.matching
import app.calculator

def Calculate(url):

    df_parsed = parser_scraper.url_to_df(url)

    categories = matching.get_categories(df_parsed, try_google = True)

    df_parsed['names'] = categories

    GHG_impact = calculator.ghg_calc(df_parsed)

    Return GHG_impact
