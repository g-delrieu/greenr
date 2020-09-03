import os


print('===== printing directory =======')
os.system('pwd')

print('===== printing content directory =======')
os.system('ls')



import re
import json
from ingredient_phrase_tagger.training import utils
from string import punctuation
import sklearn_crfsuite
from nltk.tokenize import *
import re
import json
from itertools import chain
import nltk
import pycrfsuite
import pickle as cPickle
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import subprocess
import numpy as np
from googletrans import Translator




tokenizer = PunktSentenceTokenizer()

filename = 'finalized_model.pkl'
loaded_model = cPickle.load(open(filename, 'rb'))
tagger = loaded_model.tagger_

def get_ingredients_url(url):

    page = requests.get(f'{url}')
    soup = BeautifulSoup(page.content, 'html.parser')
    ingredient = ''

    for a in soup.find_all('li', class_ = "recipe-ingredients__list-item"):
        ingredient += a.get_text()+ '.'
        ingredient += '\n'

    servingsize = soup.find('p', class_ = "recipe-metadata__serving").get_text().split(' ')[1]
    recipe_title = soup.find('h1', class_ = 'gel-trafalgar content-title__text').get_text()

    try:
        servingsize = str(servingsize).split('-')[0]
    except:
        pass

    return ingredient, servingsize, recipe_title

def sent2labels(sent):
    return [word[-1] for word in sent]

def sent2features(sent):
    return [word[:-1] for word in sent]

def sent2tokens(sent):
    return [word[0] for word in sent]


def get_sentence_features(sent):
    """Gets  the features of the sentence"""
    sent_tokens = nltk.word_tokenize(utils.cleanUnicodeFractions(sent))

    sent_features = []
    for i, token in enumerate(sent_tokens):
        token_features = [token]
        token_features.extend(utils.getFeatures(token, i+1, sent_tokens))
        sent_features.append(token_features)
    return sent_features

def format_ingredient_output(tagger_output, display=False):
    """Formats the tagger output into a more convenient dictionary"""
    data = [{}]
    display = [[]]
    prevTag = None


    for token, tag in tagger_output:
    # turn B-NAME/123 back into "name"
        tag = re.sub(r'^[BI]\-', "", tag).lower()

        # ---- DISPLAY ----
        # build a structure which groups each token by its tag, so we can
        # rebuild the original display name later.

        if prevTag != tag:
            display[-1].append((tag, [token]))
            prevTag = tag
        else:
            display[-1][-1][1].append(token)
            #               ^- token
            #            ^---- tag
            #        ^-------- ingredient

            # ---- DATA ----
            # build a dict grouping tokens by their tag

            # initialize this attribute if this is the first token of its kind
        if tag not in data[-1]:
            data[-1][tag] = []

        # HACK: If this token is a unit, singularize it so Scoop accepts it.
        if tag == "unit":
            token = utils.singularize(token)

        data[-1][tag].append(token)

    # reassemble the output into a list of dicts.
    output = [
        dict([(k, utils.smartJoin(tokens)) for k, tokens in ingredient.items()])
        for ingredient in data
        if len(ingredient)
    ]

    # Add the raw ingredient phrase
    for i, v in enumerate(output):
        output[i]["input"] = utils.smartJoin(
            [" ".join(tokens) for k, tokens in display[i]])

    return output

def parse_ingredient(sent):
    """ingredient parsing logic"""
    sentence_features = get_sentence_features(sent)
    tags = tagger.tag(sentence_features)
    tagger_output = zip(sent2tokens(sentence_features), tags)
    parsed_ingredient =  format_ingredient_output(tagger_output)
    if parsed_ingredient:
        parsed_ingredient[0]['name'] = parsed_ingredient[0].get('name','').strip('.')

    return parsed_ingredient



def parse_recipe_ingredients(ingredient_list):

    """Wrapper around parse_ingredient so we can call it on an ingredient list"""
    sentences = tokenizer.tokenize(ingredient_list)
    sentences = [sent.strip('\n') for sent in sentences]
    names = []
    qtys = []
    units = []
    our_punctuation = '!"#$%&\'())*+:;<=>?@[\\]^_`{|}~'

    for sent in sentences:
        for punctuation in our_punctuation:
        # cleaning for common issues
            sent = sent.replace(punctuation, '')

        sent = sent.replace('can', '')
        sent = sent.replace('package', '')
        sent = sent.replace('container', '')
        sent = sent.replace('eggs eggs', 'eggs')
        sent = sent.replace('⅓', '.33')
        sent = sent.replace('½', '.5')
        sent = sent.replace('¼', '.25')
        sent = sent.replace('¾', '.75')
        sent = sent.replace('tsp', 'teaspoon')
        sent = sent.replace('tbsp', 'tablespoon')

        if re.search("\dg", sent) is not None:
            sent = sent.replace("g", "gram", 1)


        parsed_ingredient = parse_ingredient(sent)

        #import pdb; pdb.set_trace()
        if 'name' in parsed_ingredient[0].keys():

            tmp = parsed_ingredient[0]['name']
            useless_quantifiers = ['oz', 'fl', 'ounce']

            try:
                names.append(re.search("[^\d]*$", tmp).group(0))
            except:
                names.append(tmp)

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

        if re.search("\dg", sent) is not None:
            try:
                qtys.append(re.search("(\d+)((\d+))+", parsed_ingredient[0]['input']).group(0))
            except:
                pass
        elif 'qty' in parsed_ingredient[0].keys():
            qtys.append(parsed_ingredient[0]['qty'])
        else:
            try:
                qtys.append(float(parsed_ingredient[0]['input'][:3]))
            except:
                qtys.append(np.nan)


    final_df = pd.DataFrame(list(zip(qtys, units, names)), columns = ['qty', 'unit', 'name'])

    final_df = final_df[final_df['name'].notna()]
    final_df = final_df[final_df['unit'].notna()]

    final_df.loc[final_df['unit'] == 'teaspoon', 'qty'] = 0
    final_df.loc[final_df['unit'] == 'teaspoon', 'unit'] = 'gram'
    final_df.loc[final_df['qty'].astype(str) == 'nan', 'qty'] = 1

    return final_df


def url_to_df(url):

    ingredient_list, servingsize, recipe_title = get_ingredients_url(url)

    raw_ingredient_list = ingredient_list

    return parse_recipe_ingredients(ingredient_list), servingsize, raw_ingredient_list.split('\n'), recipe_title


#### parser for Marmiton:
def marmiton_to_df(url):
    page = requests.get(f'{url}')
    soup = BeautifulSoup(page.content, 'html.parser')
    tmp = soup.find_all('script', type = "text/javascript")[9]
    ingredient = json.loads(re.search('(?<=recipesData \= )(.*?)(?=;)', str(tmp.contents[0])).group(0))['recipes'][0]['ingredients']

    #translating
    translator = Translator()

    ingredients = []
    qty = []
    unit = []
    for i in range(len(ingredient)):
        ingredients.append(translator.translate(ingredient[i]['name'], src ='fr').text)
        qty.append(ingredient[i]['qty'])
        #import pdb; pdb.set_trace()
        if ingredient[i]['unit']== '':
            unit.append('unit')
        elif translator.translate(ingredient[i]['unit'], src ='fr').text == 'g':
            unit.append('gram')
        elif translator.translate(ingredient[i]['unit'], src ='fr').text == 'spoon':
            unit.append('teaspoon')

        else:
            unit.append(translator.translate(ingredient[i]['unit'], src ='fr').text)
        #
    final_df = pd.DataFrame(list(zip(qty, unit, ingredients)), columns = ['qty', 'unit', 'ingredients'])
    final_df = final_df[final_df['ingredients'].notna()]
    final_df = final_df[final_df['unit'].notna()]
    final_df = final_df[final_df['unit'] != 'teaspoon']

    return final_df

#### scraper for Chefkoch:
def chefkoch_to_list(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tmp = soup.find_all('script', type = "application/ld+json")[1]
    ing_list = json.loads(str(tmp).strip('<script type="application/ld+json">    '))['recipeIngredient']
    de_list = []
    for ing in ing_list:
        de_list.append(Translator().translate(ing, src ='de').text)
    return de_list
