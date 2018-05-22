"""Build uppercase frequency dictionaries and measure word variance."""

from collections import Counter
from pylev import levenshtein
from nltk.corpus import words
from nltk.corpus import wordnet
from translate import Translator as translator
import os
import re
import sys
import shutil
import operator

class CapsDictionaries(object):

    def __init__(self):

        self.file_read = self.file_read()
        self.word_list = self.file_read[0]
        self.word_list_stripped = self.file_read[1]
        self.fiche_dictionary = self.file_read[2]
        self.fiche_locations = self.file_read[3]
        self.english_words = self.cunstruct_english_dictionary()
        self.capitals_data = self.build_capitals_data()

        self.word_dict_full = self.capitals_data[0]
        self.word_dict_caps = self.capitals_data[1]
        self.word_list_full = self.capitals_data[2]
        self.word_list_extra = self.capitals_data[3]
        self.word_list_long = self.capitals_data[4]
        self.word_list_medium = self.capitals_data[5]
        self.word_list_short = self.capitals_data[6]

        self.common_words = self.build_count_lists()
        self.identify_capitals_errors()

    def file_read(self):
        """Read files produced by BuildAggregate module into class."""

        def read_to_list(file_path):
            """Read from .txt file into list object."""

            with open(file_path, 'r') as temporary_file:
                temporary_file = temporary_file.read()

            list_out = temporary_file.split('\n')
            return list_out

        def read_to_dictionary(file_path):
            """Read from .txt file into dictionary object."""

            dictionary_out = {}
            with open(file_path, 'r') as temporary_file:
                temporary_file = temporary_file.read()

            read_list = temporary_file.split('\n')

            for item in read_list:
                item_list = item.split(', ')[:-1]

                if len(item_list) == 3:
                    dictionary_out.update({item_list[0]:[item_list[1], item_list[2]]})
                elif len(item_list) == 4:
                    if item_list[0] not in dictionary_out.keys():
                        dictionary_out.update({item_list[0]:[int(item_list[1]),
                                                             [[int(item_list[2]), int(item_list[3])]]]})

                    elif item_list[0] in dictionary_out.keys():
                        dictionary_out[item_list[0]][1].append([int(item_list[2]), int(item_list[3])])

            return dictionary_out

        word_list = read_to_list('working_directory/word_list.txt')
        word_list_stripped = read_to_list('working_directory/word_list_stripped.txt')

        fiche_dictionary = read_to_dictionary('working_directory/fiche_dictionary.txt')
        fiche_locations = read_to_dictionary('working_directory/fiche_locations.txt')

        return (word_list, word_list_stripped, fiche_dictionary, fiche_locations)

    def cunstruct_english_dictionary(self):
        """Construct dictionary of English words (not a catch-all dictionary)."""

        english_words = []
        for word in list(wordnet.words()):
            english_words.append(word)

        for word in list(words.words()):
            english_words.append(word)

        return english_words

    def build_capitals_data(self):
        """Catch all all-caps or mostly-caps words and sort them into length lists.
           Additionaly, construct numbered dictionary of all words in corpus (location: word).
        """

        regex00 = r'[a-z]{0,2}[^a-z]{0,4}[A-Z][a-z]{0,3}[^a-z]*[A-Z][a-z]{0,3}[^a-z]*[A-Z][a-z]{0,3}[^a-z]*$'

        word_dict_full = {}
        word_dict_caps = {}
        word_list_extra = []
        word_list_long = []
        word_list_medium = []
        word_list_short = []

        for i, word in enumerate(self.word_list_stripped):
            word_dict_full.update({i: word})

        iteration = 0
        str_length = [10, 8, 6, 4]
        while iteration < 4:
            for i, word in word_dict_full.items():
                if re.match(regex00, word):
                    if iteration == 0:
                        if len(word) >= str_length[iteration]:
                            word_list_extra.append(word)
                            word_dict_caps.update({i: word})
                    else:
                        if len(word) >= str_length[iteration] and len(word) < str_length[iteration-1]:
                            if iteration == 1:
                                word_list_long.append(word)
                                word_dict_caps.update({i: word})
                            elif iteration == 2:
                                word_list_medium.append(word)
                                word_dict_caps.update({i: word})
                            elif iteration == 3:
                                word_list_short.append(word)
                                word_dict_caps.update({i: word})
            iteration += 1

        word_list_full = [word for word in word_dict_caps.values()]

        return (word_dict_full, word_dict_caps, word_list_full, word_list_extra,
                word_list_long, word_list_medium, word_list_short)

    def build_count_lists(self):
        """Construct word count Counter objects and a collection of most common words"""

        count_list_dictionary = {
            'list_extra' : [self.word_list_extra, Counter()],
            'list_long' : [self.word_list_long, Counter()],
            'list_medium' : [self.word_list_medium, Counter()],
            'list_short' : [self.word_list_short, Counter()]
        }

        for word in self.word_list_full:
            for word_list, counter in count_list_dictionary.values():
                if word in word_list:
                    counter[word] += 1

        common_words = []
        def common_words_append(counter):
            """Extract top words from counter objects"""

            for word in counter.most_common(25):
                if word[0].isupper() == True:
                    common_words.append(word[0])

        for word_list, counter in count_list_dictionary.values():
            common_words_append(counter)

        return common_words

    def define_context(self, key, word, location):
        """"""

        # Take raw distance and morphy values
        distance = levenshtein(key, word)
        morphy_key = wordnet.morphy(key.lower())
        morphy_word = wordnet.morphy(word.lower())

        # Define left-split criteria
        split_word_left_one = self.word_dict_full[location-1] + word
        split_word_left_two = self.word_dict_full[location-2] + self.word_dict_full[location-1] + word

        distance_split_left_one = levenshtein(key, split_word_left_one)
        distance_split_left_two = levenshtein(key, split_word_left_two)

        if distance_split_left_one <= distance_split_left_two:
            split_word_left = split_word_left_one
            distance_split_left = distance_split_left_one
        else:
            split_word_left = split_word_left_two
            distance_split_left = distance_split_left_two

        morphy_split_left = wordnet.morphy(split_word_left.lower())

        # Define right-split criteria
        split_word_right_one = word + self.word_dict_full[location+1]
        split_word_right_two = word + self.word_dict_full[location+1] + self.word_dict_full[location+2]

        distance_split_right_one = levenshtein(key, split_word_right_one)
        distance_split_right_two = levenshtein(key, split_word_right_two)

        if distance_split_right_one <= distance_split_right_two:
            split_word_right = split_word_right_one
            distance_split_right = distance_split_right_one
        else:
            split_word_right = split_word_right_two
            distance_split_right = distance_split_right_two

        morphy_split_right = wordnet.morphy(split_word_right.lower())

        return (distance, morphy_key, morphy_word, split_word_left, distance_split_left,
                morphy_split_left, split_word_right, distance_split_right, morphy_split_right)

    def identify_capitals_errors(self):
        """Search Corpus for likely misconstructions of common all-capital words."""

        def clear_destination(file_path):
            """Identify if file exists. If so, remove it."""

            if os.path.exists(file_path):
                os.remove(file_path)

        def error_locator(location, word):
            """Identify fiche and page data for words identified as errors."""

            fiche_find_dictionary = {}
            page_find_dictionary = {}
            for fiche, data in self.fiche_locations.items():
                difference_fiche = location - data[0]
                if difference_fiche > 0 and fiche not in fiche_find_dictionary.keys():
                    fiche_find_dictionary.update({fiche:difference_fiche})

            fiche_found = min(fiche_find_dictionary, key=fiche_find_dictionary.get)

            for fiche, data in self.fiche_locations.items():
                for list_item in data[1]:
                    if fiche == fiche_found:
                        difference_page = location - list_item[1]
                        page = str(list_item[0]).zfill(4)
                        if difference_page > 0 and page not in page_find_dictionary.keys():
                            page_find_dictionary.update({page:difference_page})

            page_found = min(page_find_dictionary, key=page_find_dictionary.get)
            fiche_page_location = str(fiche_found) + '-' + page_found

            fiche_error_dictionary[fiche_found] += 1
            fiche_page_error_dictionary[fiche_page_location] += 1

            return fiche_page_location

        clear_destination('working_directory/error_records.txt')
        clear_destination('working_directory/of_interest.txt')
        clear_destination('working_directory/error_count_fiche.txt')
        clear_destination('working_directory/error_count_page.txt')

        error_dictionary = {}
        inspect_dictionary = {}
        fiche_error_dictionary = Counter()
        fiche_page_error_dictionary = Counter()
        for key in self.common_words:
            for location, word in sorted(self.word_dict_caps.items(), key=operator.itemgetter(0))[:2500]:
                if word in self.word_list_extra:
                    distance_cutoff = 3
                elif word in self.word_list_long:
                    distance_cutoff = 2
                else:
                    distance_cutoff = 1

                key_word_data = self.define_context(key, word, location)

                distance = key_word_data[0]
                morphy_key = key_word_data[1]
                morphy_word = key_word_data[2]
                split_word_left = key_word_data[3]
                distance_split_left = key_word_data[4]
                morphy_split_left = key_word_data[5]
                split_word_right = key_word_data[6]
                distance_split_right = key_word_data[7]
                morphy_split_right = key_word_data[8]

                # Sort words into buckets
                if word not in self.common_words:
                    if (distance > 0 and distance <= distance_cutoff
                        and (word.lower() == key.lower() or word.lower() not in self.english_words)
                        and (morphy_word == None or word.isupper() == False)):

                        fiche_page_location = error_locator(location, word)

                        if location in error_dictionary.keys():
                            if error_dictionary[location][2] > distance:
                                error_dictionary[location] = [word, fiche_page_location, distance]
                        else:
                            error_dictionary.update({location: [word, fiche_page_location, distance]})

                        with open('working_directory/error_records.txt', 'a') as error_records:
                            error_records.write('  '.join(('SIMPLE ERROR SEARCH:', key, word, "context:",
                                                           "'" + str(self.word_dict_full[location-2]),
                                                           str(self.word_dict_full[location-1]),
                                                           word, str(self.word_dict_full[location+1]),
                                                           str(self.word_dict_full[location+2]) + "'",
                                                           '\n')))

                    elif (distance_split_left <= distance_cutoff and key != word
                          and morphy_key != morphy_word):

                          fiche_page_location = error_locator(location, word)

                          if location in error_dictionary.keys():
                              if error_dictionary[location][2] > distance:
                                  error_dictionary[location] = [word, fiche_page_location, distance]
                          else:
                              error_dictionary.update({location: [word, fiche_page_location, distance]})

                          with open('working_directory/error_records.txt', 'a') as error_records:
                              error_records.write('  '.join(('BI- TRI-GRAM LEFT:', key,
                                                             split_word_left, 'morphy:', str(morphy_key),
                                                             str(morphy_word), "context:",
                                                             "'" + str(self.word_dict_full[location-2]),
                                                             str(self.word_dict_full[location-1]),
                                                             word, str(self.word_dict_full[location+1]),
                                                             str(self.word_dict_full[location+2]) + "'",
                                                             '\n')))

                    elif (distance_split_right <= distance_cutoff and key != word
                          and morphy_key != morphy_word):

                          fiche_page_location = error_locator(location, word)

                          if location in error_dictionary.keys():
                              if error_dictionary[location][2] > distance:
                                  error_dictionary[location] = [word, fiche_page_location, distance]
                          else:
                              error_dictionary.update({location: [word, fiche_page_location, distance]})

                          with open('working_directory/error_records.txt', 'a') as error_records:
                              error_records.write('  '.join(('BI- TRI-GRAM RIGHT:', key,
                                                             split_word_right, 'morphy:', str(morphy_key),
                                                             str(morphy_word),"context:",
                                                             "'" + str(self.word_dict_full[location-2]),
                                                             str(self.word_dict_full[location-1]), word,
                                                             str(self.word_dict_full[location+1]),
                                                             str(self.word_dict_full[location+2]) + "'",
                                                             '\n')))

                    elif (distance > 0 and distance <= distance_cutoff
                          and (morphy_word is not None or morphy_key == morphy_word)):

                          fiche_page_location = error_locator(location, word)

                          if location in inspect_dictionary.keys():
                              if inspect_dictionary[location][2] > distance:
                                  inspect_dictionary[location] = [word, fiche_page_location, distance]
                          else:
                              inspect_dictionary.update({location: [word, fiche_page_location, distance]})

                          with open('working_directory/of_interest.txt', 'a') as of_interest:
                              of_interest.write('  '.join(('SHARED ROOT SEARCH:', key, word,
                                                           'morphy:', str(morphy_word), "context:",
                                                           "'" + str(self.word_dict_full[location-2]),
                                                           str(self.word_dict_full[location-1]),
                                                           word, str(self.word_dict_full[location+1]),
                                                           str(self.word_dict_full[location+2]) + "'",
                                                           '\n')))

        with open('working_directory/error_count_fiche.txt', 'a') as error_count_fiche:
            for key, value in fiche_error_dictionary.most_common():
                error_count_fiche.write('{} {}\n'.format(key, value))

        with open('working_directory/error_count_page.txt', 'a') as error_count_page:
            for key, value in fiche_page_error_dictionary.most_common():
                error_count_page.write('{} {}\n'.format(key, value))

        print(error_dictionary)
        print(inspect_dictionary)
