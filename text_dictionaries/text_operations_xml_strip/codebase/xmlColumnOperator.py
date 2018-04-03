"""Loop through lines in column objects and trigger line operator class instances appropriately."""

from pylev import levenshtein
import xmlLineOperator
import xmlStaticOperators
import re
import os

class xmlColumnOperator(object):

    def __init__(self, dictionary, page, page_plot, page_left, page_right,
                 center, left_column_start, third_first_start, third_second_start,
                 search_key_center, search_key_thirds):

        self.page = page
        self.dictionary = dictionary

        self.page_plot = page_plot
        self.page_left = page_left
        self.page_right = page_right
        self.center = center

        self.left_column_start = left_column_start
        self.third_first_start = third_first_start
        self.third_second_start = third_second_start

        self.search_key_center = search_key_center
        self.search_key_thirds = search_key_thirds

        self.plot_words()

    def plot_words(self):
        """Plot words on page/figure."""

        def write_from_list(file_path, list_name, delimiter):
            """Write list element to newline-delimited .txt file."""

            with open(file_path, 'a') as temporary_file:
                temporary_file = temporary_file.write(delimiter.join(list_name))

        dictionary_as_list = list(self.dictionary.items())[::-1]
        for i, word_list in enumerate(dictionary_as_list):
            present_line = xmlLineOperator.xmlLineOperator(dictionary_as_list[i], self.page_plot,
                                                           self.page_left, self.page_right,
                                                           self.center, self.left_column_start,
                                                           self.third_first_start,
                                                           self.third_second_start,
                                                           self.search_key_center,
                                                           self.search_key_thirds, False)

            if present_line.company_name_found == 'Undefined' and i < (len(dictionary_as_list) - 1):
                next_line = xmlLineOperator.xmlLineOperator(dictionary_as_list[i+1], self.page_plot,
                                                               self.page_left, self.page_right,
                                                               self.center, self.left_column_start,
                                                               self.third_first_start,
                                                               self.third_second_start,
                                                               self.search_key_center,
                                                               self.search_key_thirds, True)

                for word in next_line.captured_words:
                    present_line.captured_words.append(word)

            if len(present_line.captured_words) > 0:
                page = ['\n', self.page, '\n']
                present_line.captured_words.append('\n')
                write_from_list('company_names.txt', page, '')
                write_from_list('company_names.txt',
                                [word[0] for word in present_line.captured_words], ' ')
