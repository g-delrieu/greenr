import re

import utils


def tokenize(s):
    """
    Tokenize on parenthesis, punctuation, spaces and American units followed by a slash.

    We sometimes give American units and metric units for baking recipes. For example:
        * 2 tablespoons/30 mililiters milk or cream
        * 2 1/2 cups/300 grams all-purpose flour

    The recipe database only allows for one unit, and we want to use the American one.
    But we must split the text on "cups/" etc. in order to pick it up.
    """

    # handle abbreviation like "100g" by treating it as "100 grams"
    s = re.sub(r'(\d+)g', r'\1 grams', s)
    s = re.sub(r'(\d+)oz', r'\1 ounces', s)
    s = re.sub(r'(\d+)ml', r'\1 milliliters', s, flags=re.IGNORECASE)

    american_units = [
        'cup', 'tablespoon', 'teaspoon', 'pound', 'ounce', 'quart', 'pint'
    ]
    for unit in american_units:
        s = s.replace(unit + '/', unit + ' ')
        s = s.replace(unit + 's/', unit + 's ')

    return filter(None, re.split(r'([,\(\)])?\s*', utils.clumpFractions(s)))
