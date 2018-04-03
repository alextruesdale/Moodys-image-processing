"""Class in which high-level corpus lists and dictionaries are created."""

from collections import Counter
from nltk.corpus import stopwords
import os
import re
import shutil

class PreliminaryParsing(object):

    def __init__(self, working_file):

        self.working_file = working_file
        self.list_lines = self.list_lines()
        self.words_data = self.list_words()
        self.list_words = self.words_data[0]
        self.list_words_stripped = self.words_data[1]
        self.word_dictionary = self.word_dictionary()
        self.word_dict_full = self.build_word_dict()
        self.fiche_data = self.fiche_dictionary()

        self.fiche_dictionary = self.fiche_data[0]
        self.fiche_locations = self.fiche_data[1]

        self.save_working_files()

    def list_lines(self):
        """Create list of all lines in corpus."""

        list_lines = self.working_file.split('\n')
        return list_lines

    def list_words(self):
        """Create lists of words in corpus raw and stripped of right-side punctuation."""

        list_words = []
        for line in self.list_lines:
            word_sub_list = line.split()
            list_words.extend(word_sub_list)

        unicode_ascii_list = [chr(value) for value in range(0, 128)]

        non_ascii_dict = Counter()
        for word in list_words:
            for char in word:
                if char not in unicode_ascii_list:
                    non_ascii_dict[char] += 1

        character_list = [pairing[0] for pairing in non_ascii_dict]
        regex00_list = [r'.*{}.*'.format(character) for character in character_list]

        regex01 = r'(.*[a-zA-Z\d\/]+)[^a-zA-Z\d]+$'
        # regex02 = r'(^.*[a-zA-Z]{2,4}[.,]*)'
        regex03 = r'^[^a-zA-Z\d\/]+([a-zA-Z\d\/]+.*)'

        list_words_stripped = []
        for word in list_words:

            # Strip right
            if re.match(regex01, word):
                stripped = re.sub(regex01, r'\1', word)
            # elif re.match(regex02, word):
            #     stripped = re.sub(regex02, r'\1', word)
            else:
                stripped = word

            # Strip left
            if re.match(regex03, stripped):
                stripped = re.sub(regex03, r'\1', stripped)
            else:
                stripped = stripped

            # Strip non_ascii
            if any(re.match(regex, stripped) for regex in regex00_list):
                character_contained = [character for character in stripped
                                       if character in character_list]

                for character in character_contained:
                    stripped = re.sub(r'{}'.format(character), '', stripped)

            list_words_stripped.append(stripped)

        return (list_words, list_words_stripped)

    def word_dictionary(self):
        """Create dictionary of all words and their counts."""

        stop_words = set(stopwords.words('english'))

        word_dictionary = Counter()
        for word in self.list_words_stripped:
            if word not in stop_words:
                word_dictionary[word] += 1

        return word_dictionary

    def build_word_dict(self):
        """Create Dictionary of words and word locations."""

        word_dict_full = {}
        for i, word in enumerate(self.list_words_stripped):
            word_dict_full.update({i: word})

        return word_dict_full

    def fiche_dictionary(self):
        """Create dictionary of fiches in corpus and meta details."""

        list_fiche = [line for line in self.list_lines if line.startswith('/scratch/summit')]

        fiche_dictionary = {}
        for fiche in list_fiche:
            for location, word in self.word_dict_full.items():
                if word == fiche:
                    page_start = location

            key = fiche
            fiche_trimmed = fiche[:-4]
            page_number = fiche_trimmed[-4:]
            fiche_number = fiche_trimmed[-9:-5]
            fiche_dictionary.update({key:[fiche_number, page_number, page_start]})

        fiche_locations = {}
        for fiche, data in fiche_dictionary.items():
            if data[0] not in fiche_locations.keys():
                fiche_locations.update({data[0]:[data[2], [[data[1], data[2]]]]})
            elif data[0] in fiche_locations.keys():
                fiche_locations[data[0]][1].append([data[1], data[2]])

        return (fiche_dictionary, fiche_locations)

    def save_working_files(self):
        """Save generated lists and dictionaries as .txt files."""

        def clear_destination(file_path):
            """Identify if file exists. If so, remove it."""

            if os.path.exists(file_path):
                os.remove(file_path)

        def write_from_list(file_path, list_name):
            """Write list element to newline-delimited .txt file."""

            delimiter = '\n'

            with open(file_path, 'w') as temporary_file:
                temporary_file = temporary_file.write(delimiter.join(list_name))

        def write_from_dictionary(file_path, dictionary_name):

            delimiter = ', '

            for key, value in dictionary_name.items():
                with open(file_path, 'a') as temporary_file:
                    if len(value) == 3:
                        temporary_file = temporary_file.write(delimiter.join((key, str(value[0]),
                                                                              str(value[1]), '\n')))
                    elif len(value) == 2:
                        for item in value[1]:
                            file_name = temporary_file.write(delimiter.join((key, str(value[0]),
                                                                             str(item[0]),
                                                                             str(item[1]),
                                                                             '\n')))

        clear_destination('working_directory/word_list.txt')
        write_from_list('working_directory/word_list.txt', self.list_words)

        clear_destination('working_directory/word_list_stripped.txt')
        write_from_list('working_directory/word_list_stripped.txt', self.list_words_stripped)

        clear_destination('working_directory/fiche_dictionary.txt')
        write_from_dictionary('working_directory/fiche_dictionary.txt', self.fiche_dictionary)

        clear_destination('working_directory/fiche_locations.txt')
        write_from_dictionary('working_directory/fiche_locations.txt', self.fiche_locations)
