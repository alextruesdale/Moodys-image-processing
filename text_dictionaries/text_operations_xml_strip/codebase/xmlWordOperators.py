"""Class housing testing operators for words in xml output."""

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from pylev import levenshtein
import re

class xmlWordOperators(object):

    def __init__(self, page_plot, word, colour):

        self.page_plot = page_plot

        self.word_top = word[1]
        self.word_right = word[2]
        self.word_bottom = word[3]
        self.word_left = word[4]

        self.colour = colour
        self.plot_word()

    def plot_word(self):
        """plot word on page_plot object."""

        self.page_plot.add_patch(Rectangle((self.word_left, self.word_bottom),
                                           (self.word_right-self.word_left),
                                           (self.word_top-self.word_bottom),
                                           fill=None, edgecolor=self.colour, alpha=1))

    @staticmethod
    def capital_search(word):
        """Perform string search to evaluate if word is significant (all caps)."""

        if len(word) == 1:
            regex00 = r'[A-Z]'
        elif len(word) <= 3:
            regex00 = r'[a-z]{0,2}[^a-z]{0,4}[A-Z][a-z]{0,3}[^a-z]*[A-Z][a-z]{0,3}[^a-z]*$'
        else:
            regex00 = r'[a-z]{0,2}[^a-z]{0,4}[A-Z][a-z]{0,3}[^a-z]*[A-Z][a-z]{0,3}[^a-z]*[A-Z][a-z]{0,3}[^a-z]*$'

        result = re.match(regex00, word)
        return result

    @staticmethod
    def end_position(word, word_next):
        """Search for ending colon on company name."""

        result = False
        colon_found = False
        incorporated = False
        regex01 = r'.*\:$'
        distance = levenshtein('Incorporated', word)
        distance_plus = levenshtein('Incorporated', (word + word_next))

        if distance <= 3 or distance_plus <= 5 or re.match(regex01, word):
            result = True

        if distance <= 3 or distance_plus <= 5:
            incorporated = True

        if re.match(regex01, word):
            colon_found = True

        return (result, incorporated, colon_found)

    @staticmethod
    def strip_punctuation(word):
        """Strip punctuation from word."""

        word = re.sub(r'[\.\,\:\;\"\']', '', word)
        return word

    @staticmethod
    def check_capital_title(captured_words):
        """Check to see that a string hasn't been falsely identified"""

        is_not_title = True
        first_two = captured_words[:2]
        if all(xmlWordOperators.capital_search(word[0]) for word in first_two):
            is_not_title = False

        return is_not_title

    @staticmethod
    def check_against_popular(word):
        """Check word against list of popular words."""

        in_list = False

        popular_words_long = ['MANAGEMENT', 'OFFICER', 'CAPITAL', 'CONSOLIDATED', 'PRODUCTION',
                              'CONTINGENT', 'INCORPORATED', 'MORTGAGES', 'COMPARATIVE',
                              'LIABILITIES', 'SUBSIDIARIES', 'SUBSCRIPTION', 'AGREEMENT',
                              'PROPERTIES', 'PRIVILEGE', 'RECEIVERSHIP', 'RECAPITALIZATION',
                              'AFFILIATED']

        popular_words_medium = ['WARRANTS', 'EXCHANGE', 'INCOME', 'RIGHTS', 'VOTING', 'OUTPUT',
                                'STOCK', 'ASSETS', 'MERGER', 'RANGE', 'PRICE', 'TRUST', 'SALES',
                                'FUNDED', 'CONTROL', 'EARNINGS', 'BALANCE', 'SERIAL', 'RETIRED',
                                'BONDED', 'PROPOSED']

        popular_words_short = ['NOTE', 'DEBT', 'FILM', 'NET', 'BONDS']

        distance_list_long = [levenshtein(check_word, word) for check_word in popular_words_long]
        distance_list_medium = [levenshtein(check_word, word) for check_word in popular_words_medium]
        distance_list_short = [levenshtein(check_word, word) for check_word in popular_words_short]

        in_list_long = any(distance <= 4 for distance in distance_list_long)
        in_list_medium = any(distance <= 2 for distance in distance_list_medium)
        in_list_short = any(distance <= 1 for distance in distance_list_short)
        in_list_list = [in_list_long, in_list_medium, in_list_short]

        in_in_list_list = any(in_list_list)
        return in_in_list_list
