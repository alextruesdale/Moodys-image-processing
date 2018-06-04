"""Construct word map graphs for each sheet in page_data_dictionary."""

from operator import itemgetter
import xmlColumnOperator
import xmlWordOperators
import numpy as np

class xmlPageOperator(object):

    def __init__(self, i, year, page_data, file_path, xml_column_chart_center, xml_column_chart_thirds):

        self.page_data = page_data
        self.page_index = i
        self.year = year
        self.page = page_data.page
        self.file_path = file_path
        self.word_data = page_data.word_data

        self.section_list_center = xml_column_chart_center.section_list
        self.section_list_thirds = xml_column_chart_thirds.section_list

        self.page_top = page_data.page_top
        self.page_right = page_data.page_right
        self.page_bottom = page_data.page_bottom
        self.page_left = page_data.page_left

        self.center = page_data.center
        self.third_first = page_data.third_first
        self.third_second = page_data.third_second

        self.search_key_data = self.left_search_bound()
        self.search_key_center = self.search_key_data[0]
        self.search_key_thirds = self.search_key_data[1]

        self.lines_data = self.define_lines()
        self.lines_dict = self.lines_data[0]
        self.words_excluded = self.lines_data[1]
        self.line_data_dict = self.lines_data[2]

        self.page_break_dictionary_insgesamt = self.instantiate_columns()

    def left_search_bound(self):
        """Based on manual sections bounds, define key variable for company name search bounds."""

        difference_list_center = sorted([[item, self.page_index - item[0]] for item in
                                         self.section_list_center if self.page_index - item[0] > 0],
                                         key=itemgetter(1))

        difference_list_thirds = sorted([[item, self.page_index - item[0]] for item in
                                         self.section_list_thirds if self.page_index - item[0] > 0],
                                         key=itemgetter(1))

        key_center = difference_list_center[0][0][2]
        key_thirds = difference_list_thirds[0][0][2]
        return (key_center, key_thirds)

    def define_lines(self):
        """Define text lines (rows) using bottom bounds of words."""

        word_list = sorted([[i, word[0], word[1], word[2], word[3], word[4]] for i, word
                            in enumerate(self.word_data) if (word[2] > self.page_left and
                            word[4] < self.page_right and word[1] > self.page_bottom and
                            word[3] < self.page_top)], key=itemgetter(4))

        word_dict = {word[0]: [word[1], word[2], word[3], word[4], word[5]] for word in word_list}

        if self.search_key_center == True:
            operate_list = [{word[0]: [word[1], word[4]] for word in word_list if word[3] < self.center},
                            {word[0]: [word[1], word[4]] for word in word_list if word[3] > self.center}]

        elif self.search_key_thirds == True:
            operate_list = [{word[0]: [word[1], word[4]] for word in word_list if word[3] < self.third_first},
                            {word[0]: [word[1], word[4]] for word in word_list if (word[3] > self.third_first and word[3] < self.third_second)},
                            {word[0]: [word[1], word[4]] for word in word_list if word[3] > self.third_second}]

        else:
            operate_list = [{word[0]: [word[1], word[4]] for word in word_list}]

        lines_dict = {}
        line_data_dict = {self.page: []}
        registered_indeces = []
        index = 0
        for column in operate_list:
            lines_dict_component = {}
            sub_list = []
            column_list = list(column.items())
            for i, word in enumerate(column_list[:-1]):
                word_index = column_list[i][0]
                bottom_coordinate = column_list[i][1][1]
                next_bottom = column_list[i+1][1][1]
                prev_bottom = column_list[i-1][1][1]
                bottom_offset = .00478

                if next_bottom - bottom_offset < bottom_coordinate < next_bottom + bottom_offset:
                    sub_list.append([word_index, bottom_coordinate])
                    registered_indeces.append(word_index)

                else:
                    if prev_bottom - bottom_offset < bottom_coordinate < prev_bottom + bottom_offset:
                        sub_list.append([word_index, bottom_coordinate])
                        registered_indeces.append(word_index)

                    if len(sub_list) >= 2:
                        lines_dict_component.update({np.mean([item[1] for item in sub_list]):
                                                             sorted([word_dict[item[0]] for item
                                                             in sub_list], key=itemgetter(4))})
                        sub_list = []

            for item in sub_list:
                registered_indeces.remove(item[0])

            lines_dict.update({index:lines_dict_component})
            index += 1

        words_excluded = [word for index, word in word_dict.items() if index not in registered_indeces]
        line_data_dict[self.page].extend((lines_dict, words_excluded))

        return (lines_dict, words_excluded, line_data_dict)

    def instantiate_columns(self):
        """Loop over divided columns and operate."""

        page_break_dictionary_insgesamt = {}
        for index, dictionary in self.lines_dict.items():
            column_data = xmlColumnOperator.xmlColumnOperator(index, dictionary, self.page, self.year,
                                                              self.file_path, self.page_data,
                                                              self.search_key_data)

            if self.page in page_break_dictionary_insgesamt.keys():
                page_break_dictionary_insgesamt[self.page].update(column_data.page_break_dictionary_teilweise)

            if len(column_data.page_break_dictionary_teilweise) > 0 and self.page not in page_break_dictionary_insgesamt.keys():
                page_break_dictionary_insgesamt.update({self.page: column_data.page_break_dictionary_teilweise})

        return page_break_dictionary_insgesamt
