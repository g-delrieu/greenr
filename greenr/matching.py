# Import some packages

import _pickle as cPickle
import string
import pandas as pd
import numpy as np
import scipy
from scipy import spatial

from bs4 import BeautifulSoup
import urllib.parse
import urllib.request

from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from googleapiclient.discovery import build
import os.path
import os
import wikipedia
import pymongo

# Load some data, define some values
mongo_key = os.environ.get('DB_PASSWORD')

myclient = pymongo.MongoClient(f"mongodb+srv://gdelrieu:{mongo_key.strip()}@cluster0.jceas.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["greenr"]
mycol = mydb["family_pairs"]


api_key = os.environ.get('GREENR_API_KEY')

with open('matching_objects2.pk', 'rb') as handle:
    matching_objects_dict = cPickle.load(handle)
    vectorizer = matching_objects_dict['vectorizer']
    df_wiki_match_scores = matching_objects_dict['df_wiki_match_scores']
    category_list = matching_objects_dict['category_list']
    category_summaries = matching_objects_dict['category_summaries']
    category_summary_vectors = vectorizer.transform(category_summaries)

cse_id = "dd94ab4664d1ce589"
similarity_cutoff = 0.1
no_match = 'No match found'

### Define some utility functions

# Own db

def is_ingredient_in_database(ingredient):

    found = mycol.find({"ingredient":ingredient}).count() >0

    return found


def get_database_match(ingredient):

    match = mycol.find_one({"ingredient":ingredient})['family']

    return match


# Wiki db

def is_ingredient_in_wikidata(ingredient):
    found = ingredient in list(df_wiki_match_scores.ingredient)
    return found


def get_wiki_match(ingredient):

    match = df_wiki_match_scores.loc[df_wiki_match_scores['ingredient'] ==
                                     ingredient, 'category'].iloc[0]

    score = df_wiki_match_scores.loc[df_wiki_match_scores['ingredient'] ==
                                     ingredient, 'score'].iloc[0]

    return match, score


# Google option

def google_query(query, api_key, cse_id, **kwargs):

    query_service = build("customsearch",
                          "v1",
                          developerKey=api_key,
                          cache_discovery=False)
    query_results = query_service.cse().list(q=query, cx=cse_id,
                                             **kwargs).execute()

    return query_results['items']


def get_google_cse_result(ingredient):

    query = f'{ingredient} food'

    my_results = google_query(query, api_key, cse_id, num=1)[0]

    url = my_results['link']
    url_base = os.path.basename(my_results['link'])

    return ingredient, url, url_base


def get_pageid_from_base(base):

    info_url = f'https://en.wikipedia.org/w/index.php?title={base}&action=info'

    req = urllib.request.Request(info_url)
    req.add_header('Cookie', 'euConsent=true')
    html_content = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html_content, 'html.parser')

    infosection = soup.find("script")
    pageid = infosection.decode().partition('wgArticleId":')[2].partition(
        ',')[0]

    return pageid


def get_summary_from_id(pageid):

    pagesummary = wikipedia.page(pageid=pageid).summary

    return pagesummary


def pre_process_summary(summary):

    # Remove punctuation
    for punctuation in string.punctuation:
        summary = str(summary).replace(punctuation, '')

    # Lower text
    summary = summary.lower()

    # Stopwords
    stop_words = set(stopwords.words('english'))
    summary_tokenized = word_tokenize(summary)
    text = [w for w in summary_tokenized if not w in stop_words]
    summary = ' '.join(text)

    # Remove digits
    summary = ''.join([word for word in summary if not word.isdigit()])


    return summary


def get_match_and_score(summary_vector):
    category_summary_vectors = vectorizer.transform(category_summaries)
    scoreseries = []

    for j, _ in enumerate(category_summaries):
        cosine_sum = 1 - spatial.distance.cosine(
            summary_vector.toarray(), category_summary_vectors[j, :].toarray())

        scoreseries.append(cosine_sum)

    matchscore = max(scoreseries)
    match = category_list[scoreseries.index(matchscore)]

    return match, matchscore


def get_google_match(ingredient):

    try:
        ingredient, url, url_base = get_google_cse_result(ingredient)

        pageid = get_pageid_from_base(url_base)

        pagesummary = get_summary_from_id(pageid)

        processed_summary = pre_process_summary(pagesummary)

        summary_vector = vectorizer.transform([processed_summary])

        match, matchscore = get_match_and_score(summary_vector)

    except:
        return 'nomatch', 0

    return match, matchscore


# Update own db

def update_database(ingredient, match):

    mydict = {"family":match,"ingredient": ingredient}

    x = mycol.insert_one(mydict)

    return None


### Define the overall matching function

def get_categories(df_parser_output, try_google=False):

    matched_categories = []

    list_of_ingredients = list(df_parser_output['name'])
    target_ingredients = set(ingredient.lower() for ingredient in category_list)

    for ingredient in list_of_ingredients:

        if ingredient[-1] in target_ingredients:

            match = ingredient[-1]

        elif is_ingredient_in_database(ingredient) and get_database_match(ingredient) != no_match:

            match = get_database_match(ingredient)

        else:

            if is_ingredient_in_wikidata(ingredient):

                wikimatch, score = get_wiki_match(ingredient)

                if score > similarity_cutoff and wikimatch != no_match:
                    match = wikimatch

                elif try_google:
                    googlematch, score = get_google_match(ingredient)
                    if score > similarity_cutoff:
                        match = googlematch
                    else:
                        match = no_match

                else:
                    match = no_match

            else:

                googlematch, score = get_google_match(ingredient)

                if score > similarity_cutoff:
                    match = googlematch

                else:
                    match = no_match


            update_database(ingredient, match)

        matched_categories.append(match)

    for i, cat in enumerate(matched_categories):
        if cat == 'Onions & leeks':
            matched_categories[i] = 'Onions & Leeks'

        if cat == 'Berries & Grapes2':
            matched_categories[i] = 'Berries & Grapes'

    return matched_categories
