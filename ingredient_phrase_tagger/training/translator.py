import decimal
import re

import tokenizer
import utils


def translate_row(row):
    """Translates a row of labeled data into CRF++-compatible tag strings.

    Args:
        row: A row of data from the input CSV of labeled ingredient data.

    Returns:
        The row of input converted to CRF++-compatible tags, e.g.

            2\tI1\tL4\tNoCAP\tNoPAREN\tB-QTY
            cups\tI2\tL4\tNoCAP\tNoPAREN\tB-UNIT
            flour\tI3\tL4\tNoCAP\tNoPAREN\tB-NAME
    """
    # extract the display name
    display_input = utils.cleanUnicodeFractions(row['input'])
    tokens = tokenizer.tokenize(display_input)

    labels = _row_to_labels(row)
    label_data = _addPrefixes([(t, _matchUp(t, labels)) for t in tokens])

    translated = ''
    for i, (token, tags) in enumerate(label_data):
        features = utils.getFeatures(token, i + 1, tokens)
        translated += utils.joinLine(
            [token] + features + [_bestTag(tags)]) + '\n'
    return translated


def _row_to_labels(row):
    """Extracts labels from a labelled ingredient data row.

    Args:
        A row of full data about an ingredient, including input and labels.

    Returns:
        A dictionary of the label data extracted from the row.
    """
    labels = {}
    label_keys = ['name', 'qty', 'range_end', 'unit', 'comment']
    for key in label_keys:
        labels[key] = row[key]
    return labels


def _parseNumbers(s):
    """
    Parses a string that represents a number into a decimal data type so that
    we can match the quantity field in the db with the quantity that appears
    in the display name. Rounds the result to 2 places.
    """
    ss = utils.unclump(s)

    m3 = re.match('^\d+$', ss)
    if m3 is not None:
        return decimal.Decimal(round(float(ss), 2))

    m1 = re.match(r'(\d+)\s+(\d)/(\d)', ss)
    if m1 is not None:
        num = int(m1.group(1)) + (float(m1.group(2)) / float(m1.group(3)))
        return decimal.Decimal(str(round(num, 2)))

    m2 = re.match(r'^(\d)/(\d)$', ss)
    if m2 is not None:
        num = float(m2.group(1)) / float(m2.group(2))
        return decimal.Decimal(str(round(num, 2)))

    return None


def _matchUp(token, labels):
    """
    Returns our best guess of the match between the tags and the
    words from the display text.

    This problem is difficult for the following reasons:
        * not all the words in the display name have associated tags
        * the quantity field is stored as a number, but it appears
          as a string in the display name
        * the comment is often a compilation of different comments in
          the display name

    """
    ret = []

    # strip parens from the token, since they often appear in the
    # display_name, but are removed from the comment.
    token = utils.normalizeToken(token)
    decimalToken = _parseNumbers(token)

    # Iterate through the labels in descending order of label importance.
    for label_key in ['name', 'unit', 'qty', 'comment', 'range_end']:
        label_value = labels[label_key]
        if isinstance(label_value, basestring):
            for n, vt in enumerate(tokenizer.tokenize(label_value)):
                if utils.normalizeToken(vt) == token:
                    ret.append(label_key.upper())

        elif decimalToken is not None:
            if label_value == decimalToken:
                ret.append(label_key.upper())

    return ret


def _addPrefixes(data):
    """
    We use BIO tagging/chunking to differentiate between tags
    at the start of a tag sequence and those in the middle. This
    is a common technique in entity recognition.

    Reference: http://www.kdd.cis.ksu.edu/Courses/Spring-2013/CIS798/Handouts/04-ramshaw95text.pdf
    """
    prevTags = None
    newData = []

    for n, (token, tags) in enumerate(data):

        newTags = []

        for t in tags:
            p = "B" if ((prevTags is None) or (t not in prevTags)) else "I"
            newTags.append("%s-%s" % (p, t))

        newData.append((token, newTags))
        prevTags = tags

    return newData


def _bestTag(tags):

    if len(tags) == 1:
        return tags[0]

    # if there are multiple tags, pick the first which isn't COMMENT
    else:
        for t in tags:
            if (t != "B-COMMENT") and (t != "I-COMMENT"):
                return t

    # we have no idea what to guess
    return "OTHER"
