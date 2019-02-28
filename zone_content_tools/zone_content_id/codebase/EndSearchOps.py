"""Module containing test functions for end of company 'objects'."""

from re import finditer
import numpy as np
import pandas as pd
import re
import nltk
import string

def test_provis_rating(value):
    """Search zone content for 'Provisional Rating' string."""

    test_string = r'.*\s.{1,3}[CcDdOoEe\d][VvWwUu].{3,5}[NnMm][Aa].{1,3}\s+.[Aa][Tt].{1,2}[NnMm].{1,4}\W\s.*'
    print_test = r'\s.{1,3}[CcDdOoEe\d][VvWwUu].{3,5}[NnMm][Aa].{1,3}\s+.[Aa][Tt].{1,2}[NnMm].{1,4}\W*\s'

    if re.match(test_string, value):
        value_out = 1

    else:
        value_out = 0

    return value_out

def tokenise(zone):
    """Return tokenised list of words."""

    def punc_strip(token):
        """Strip punctuation from word."""

        token = re.sub(r'[\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\_\`\{\|\}\~]', '', token)
        return token

    tokens = nltk.word_tokenize(zone)
    tokens = [punc_strip(token) for token in tokens if token not in string.punctuation
              if token not in string.whitespace]

    return tokens

def caps_ratio(word):
    """Define ratio of capital characters."""

    cap_count = 0
    for char in word:
        if char.isupper():
            cap_count += 1

    caps_ratio = cap_count / (len(word) + .001)
    return caps_ratio

def caps_words_search(zone_tokens):
    """Search zone for consecutive occurences of capitalised words."""

    company_found = False
    co_string = r'\sC[Oo].{0,2}\s'
    for i, word in enumerate(zone_tokens):
        if i == len(zone_tokens) - 2:
            word_current = zone_tokens[i]
            word_next = zone_tokens[i+1]
            word_next_next = ''
        elif i == len(zone_tokens) - 1:
            word_current = zone_tokens[i]
            word_next = ''
            word_next_next = ''
        else:
            word_current = zone_tokens[i]
            word_next = zone_tokens[i+1]
            word_next_next = zone_tokens[i+2]

        if (caps_ratio(word_current) >= .65 and len(word_current) >= 2 and not re.match(co_string, word_current) and
            (((caps_ratio(word_next) >= .65 and len(word_next) >= 3) or re.match(co_string, word_next)) or
            ((caps_ratio(word_next_next) >= .65 and len(word_next_next) >= 3) or re.match(co_string, word_next_next)))):

            company_found = True
            break

    return company_found

def company_search(row):
    """Search current and subsequent zones for all caps string indicating company name."""

    current_zone = str(row['text'])
    zone_next = str(row['zone_next'])
    zone_next_next = (row['zone_next_next'])
    zone_next_next_next = (row['zone_next_next_next'])

    test_string = r'.*\s.{1,3}[CcDdOoEe\d][VvWwUu].{3,5}[NnMm][Aa].{1,3}\s+.[Aa][Tt].{1,2}[NnMm].{1,4}\W\s.*'
    print_test = r'\s.{1,3}[CcDdOoEe\d][VvWwUu].{3,5}[NnMm][Aa].{1,3}\s+.[Aa][Tt].{1,2}[NnMm].{1,4}\W*\s'

    if re.match(test_string, current_zone):
        for match in finditer(print_test, current_zone):
            match_end = match.span()[1]
            current_zone = current_zone[match_end:]

        current_zone_tokens = tokenise(current_zone)
        current_company = caps_words_search(current_zone_tokens)
        if not current_company:
            next_zone_tokens = tokenise(zone_next)
            next_company = caps_words_search(next_zone_tokens)
            if not next_company:
                next_next_zone_tokens = tokenise(zone_next_next)
                next_next_company = caps_words_search(next_next_zone_tokens)
                if not next_next_company:
                    next_next_next_zone_tokens = tokenise(zone_next_next_next)
                    next_next_next_company = caps_words_search(next_next_next_zone_tokens)
                    if next_next_next_company:
                        return 4
                else:
                    return 3
            else:
                return 2
        else:
            return 1
