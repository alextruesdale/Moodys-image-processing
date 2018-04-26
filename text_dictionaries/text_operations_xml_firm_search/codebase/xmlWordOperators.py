"""Class housing testing operators for words in xml output."""

import re

from pylev import levenshtein

def capital_search(word):
    """Perform string search to evaluate if word is significant (all caps)."""

    if len(word) == 1:
        regex00 = r'[A-Z\s]'
    elif len(word) <= 3:
        regex00 = r'[a-z]{0,2}[^a-z]{0,4}[A-Z][a-z]{0,3}[^a-z]*[A-Z][a-z]{0,3}[^a-z]*$'
    else:
        regex00 = r'[a-z]{0,2}[^a-z]{0,4}[A-Z][a-z]{0,3}[^a-z]*[A-Z][a-z]{0,3}[^a-z]*[A-Z][a-z]{0,3}[^a-z]*$'

    digit_count = 0
    for char in (strip_punctuation(word)):
        if char.isnumeric():
            digit_count += 1

    digit_percentage = (digit_count + .1) / (len(strip_punctuation(word)) + .1)
    result = re.match(regex00, word)
    if digit_percentage > .30:
        result == False

    return result

def end_position(word, word_next):
    """Search for ending colon on company name."""

    result = False
    colon_found = False
    perenthesis_found = False
    incorporated = False
    regex01 = r'.*[\:\;]'
    regex02 = r'.*[\(\[].*'
    distance = levenshtein('Incorporated', strip_punctuation(word).lower())
    distance_plus = levenshtein('Incorporated', (strip_punctuation(word) + strip_punctuation(word_next)).lower())

    if distance <= 3 or distance_plus <= 5 or re.match(regex01, word) or re.match(regex02, word):
        result = True

    if distance <= 3 or distance_plus <= 5:
        incorporated = True

    if re.match(regex01, word):
        colon_found = True

    if re.match(regex02, word):
        perenthesis_found = True

    return (result, incorporated, colon_found, perenthesis_found)

def strip_punctuation(word):
    """Strip punctuation from word."""

    word = re.sub(r'[\.\,\:\;\"\'\!\?\(\)\[\]\-\s]', '', word)
    return word

def check_capital_title(captured_words):
    """Check to see that a string hasn't been falsely identified"""

    is_not_title = False
    if len(captured_words) > 2:
        operator_words = captured_words[:3]
    else:
        operator_words = captured_words[:2]

    if all(capital_search(word[0]) for word in operator_words):
        is_not_title = True

    return is_not_title

def capitals_ratio(captured_words, string_continuous):
    """"""

    def produce_ratio(captured_words):
        """"""

        capitals_ratio = ((sum([1 for char in string_continuous if char.isupper()]) + .001) /
                          (len([char for char in string_continuous]) + .001))

        return capitals_ratio

    capitals_ratio = produce_ratio(captured_words)

    if capitals_ratio < .72 and len(captured_words) > 1:
        capitals_ratio = produce_ratio(captured_words[:-1])

    if capitals_ratio < .72:
        # print('PITCH caps_ratio:', ' '.join([word[0] for word in captured_words]), '|', capitals_ratio)
        captured_words = []

    return captured_words

def identify_company_extensions(captured_words):
    """"""

    is_protected = False
    end_word = captured_words[-1][0]
    extension_list = ['CO', 'COMPANY', 'CORPORATION', 'INCORPORATED', 'INC', 'LTD', 'THE', 'CORP', 'MILLS', 'WORKS']
    distance_list = [levenshtein(check_word, end_word) for check_word in extension_list]

    if any(distance <= 1 for distance in distance_list):
        is_protected = True

    return is_protected

def check_against_popular(word, captured_words, string_continuous):
    """Check word against list of popular words."""

    is_moodys = False
    distance = levenshtein('MOODYS', strip_punctuation(captured_words[0][0]))
    if distance <= 1:
        is_moodys = True

    is_year = not capital_search(word)

    popular_words_long = ['MANAGEMENT', 'OFFICER', 'PRODUCTION', 'CONTINGENT',
                          'MORTGAGES', 'COMPARATIVE', 'LIABILITIES', 'SUBSIDIARIES',
                          'SUBSCRIPTION', 'AGREEMENT', 'PROPERTIES', 'PRIVILEGE',
                          'RECEIVERSHIP', 'RECAPITALIZATION', 'AFFILIATED', 'REFERENCE',
                          'PROVISIONAL', 'SECURITIES', 'CERTIFICATES', 'SUBSIDIARY']

    popular_words_medium = ['WARRANTS', 'EXCHANGE', 'INCOME', 'RIGHTS', 'VOTING', 'OUTPUT',
                            'STOCK', 'ASSETS', 'MERGER', 'SALES' 'FUNDED', 'RESERVES',
                            'READJUSTMENT', 'CONTROL', 'EARNINGS', 'BALANCE', 'SERIAL', 'RETIRED',
                            'INTERESTS', 'CREDITORS', 'BONDED', 'PROPOSED', 'LATEST', 'RATING',
                            'ISSUE', 'COMMITTEE', 'DISTRIBUTION', 'CONTINUED', 'DIRECTORS',
                            'CONTROLLED', 'REGISTRAR', 'CAPITAL', 'LIQUIDATION', 'Continued']

    popular_words_short = ['NOTE', 'DEBT', 'FILM', 'BONDS', 'GROSS', 'PRICE', 'MEETING',
                           'PROTECTIVE', 'SALE', 'PRODUCED', 'FUNDS', 'PLANTS', 'COMPANIES',
                           'NULL', 'CONTRACT', 'ETC', 'YEARS']

    popular_words_sensitive = ['NET', 'RANGE', 'ACTION', 'SHEET', 'SHARES', 'ACCOUNT', 'DIRT',
                               'PLAN', 'SOLD', 'COMPANIES']

    combined_list = popular_words_long + popular_words_medium + popular_words_short + popular_words_sensitive

    distance_list_long = [levenshtein(check_word, word) for check_word in popular_words_long]
    distance_list_medium = [levenshtein(check_word, word) for check_word in popular_words_medium]
    distance_list_short = [levenshtein(check_word, word) for check_word in popular_words_short]
    distance_list_sensitive = [levenshtein(check_word, word) for check_word in popular_words_sensitive]
    distance_list_string = [levenshtein(check_word, string_continuous) for check_word in combined_list]

    in_list_long = any(distance <= 3 for distance in distance_list_long)
    in_list_medium = any(distance <= 2 for distance in distance_list_medium)
    in_list_short = any(distance <= 1 for distance in distance_list_short)
    in_list_sensitive = any(distance == 0 for distance in distance_list_sensitive)
    in_list_string = any(distance <=2 for distance in distance_list_string)
    in_list_list = [in_list_long, in_list_medium, in_list_short, in_list_sensitive, in_list_string,
                    is_moodys, is_year]

    in_in_list_list = any(in_list_list)
    return in_in_list_list

def beginning_end_line_filter(captured_words, string_continuous):
    """"""

    if len(captured_words) > 1:
        if len(strip_punctuation(captured_words[-1][0])) > 0:
            if check_against_popular(strip_punctuation(captured_words[-1][0]), captured_words, string_continuous):
                # print('PITCH end_word:', captured_words)
                captured_words = []

        else:
            if check_against_popular(strip_punctuation(captured_words[-2][0]), captured_words, string_continuous):
                # print('PITCH end_word:', captured_words)
                captured_words = []

    return captured_words

def as_of_search(captured_words, string_continuous):
    """"""

    as_of = False
    regex00 = r'.*as.*of.*'
    regex01 = r'.*yea.*en.*'
    if re.match(regex00, string_continuous.lower()) or re.match(regex01, string_continuous.lower()):
        # print('PITCH as_of:', captured_string)
        captured_words = []

    return captured_words

def is_management_bonded(captured_words, string_continuous):
    """"""

    proof_string = ' '.join([strip_punctuation(word[0]) for word in captured_words])
    check_string = string_continuous
    if len(string_continuous) >= 8:
        check_string = string_continuous[:8]

    pro_forma_distance = levenshtein('PROFORMA', check_string)

    if len(string_continuous) >= 11:
        check_string = string_continuous[:11]

    management_distance = levenshtein('MANAGEMENT', check_string)
    bonded_distance = levenshtein('BONDEDDEBT', check_string)

    if len(string_continuous) >= 14:
        check_string = string_continuous[:14]

    agent_distance = levenshtein('TRANSFERAGENT', check_string)
    balance_distance = levenshtein('BALANCESHEET', check_string)
    if (management_distance <= 5 or bonded_distance <=5 or agent_distance <= 2
        or balance_distance <= 2 or pro_forma_distance <= 1):

        captured_words = []

    return captured_words
