"""Construct word map graphs for each sheet in page_data_dictionary."""

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from operator import itemgetter
import xmlColumnOperator
import xmlWordOperators
import numpy as np

class xmlChartPage(object):

    def __init__(self, i, page_data, xml_column_chart_center, xml_column_chart_thirds):

        self.page_index = i
        self.page = page_data.page
        self.word_data = page_data.word_data

        self.page_top = page_data.page_top
        self.page_bottom = page_data.page_bottom
        self.page_left = page_data.page_left
        self.page_right = page_data.page_right

        self.page_width = page_data.page_width
        self.center = page_data.center
        self.left_column_start = page_data.left_column_start

        self.third_first = page_data.third_first
        self.third_second = page_data.third_second
        self.third_first_start = page_data.third_first_start
        self.third_second_start = page_data.third_second_start

        self.section_list_center = xml_column_chart_center.section_list
        self.section_list_thirds = xml_column_chart_thirds.section_list

        self.search_key_data = self.left_search_bound()
        self.search_key_center = self.search_key_data[0]
        self.search_key_thirds = self.search_key_data[1]
        self.lines_data = self.define_lines()
        self.lines_dict = self.lines_data[0]
        self.words_excluded = self.lines_data[1]
        self.page_plot = self.plot_page()
        self.intantiate_columns()

    def left_search_bound(self):
        """Based on manual sections bounds, define key variable for company name search bounds."""

        section_list_center = [[-1, 'center', False], [74.5, 'center', True],
                               [261.5, 'center', False], [520.5, 'center', True],
                               [821.5, 'center', False], [1166.5, 'center', True],
                               [1282.5, 'center', False], [1406.5, 'center', True],
                               [1649.5, 'center', False], [1719.5, 'center', True],
                               [1822.5, 'center', False], [1901.5, 'center', True],
                               [2098.5, 'center', False], [2124.5, 'center', True],
                               [2176.5, 'center', False], [2275.5, 'center', True],
                               [2307.5, 'center', False], [2333.5, 'center', True],
                               [2343.5, 'center', False], [2425.5, 'center', True],
                               [2518.5, 'center', False], [2606.5, 'center', True],
                               [2618.5, 'center', False], [2655.5, 'center', True],
                               [2680.5, 'center', False], [2694.5, 'center', True],
                               [2710.5, 'center', False]]

        section_list_thirds = [[-1, 'thirds', False], [58.5, 'thirds', True],
                               [72.5, 'thirds', False], [262.5, 'thirds', True],
                               [282.5, 'thirds', False], [1283.5, 'thirds', True],
                               [1406.5, 'thirds', False], [2519.5, 'thirds', True],
                               [2601.5, 'thirds', False], [2710.5, 'thirds', True]]

        difference_list_center = sorted([[item, self.page_index - item[0]] for item in
                                         section_list_center if self.page_index - item[0] > 0],
                                         key=itemgetter(1))

        difference_list_thirds = sorted([[item, self.page_index - item[0]] for item in
                                         section_list_thirds if self.page_index - item[0] > 0],
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
                bottom_offset = .00475

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
        return (lines_dict, words_excluded)

    def plot_page(self):
        """Initialise canvas on which to plot word locations."""

        page_figure = plt.figure(figsize=(8.5, 11), dpi=150)
        page_plot = page_figure.add_subplot(111)
        page_figure.tight_layout(pad=5.5)

        page_plot.set_xlim([0, 1.01])
        page_plot.set_ylim([0, 1.01])
        page_plot.set_xticks(np.arange(0.0, 1.1, 0.1))
        page_plot.set_yticks(np.arange(0.0, 1.1, 0.1))

        page_plot.set_title(self.page, fontsize=13, fontweight='bold', y=1.025)
        page_plot.set_xlabel('sheet width (norm. 0-1)')
        page_plot.set_ylabel('sheet height (norm. 0-1)')
        page_plot.xaxis.set_label_coords(.5, -.05)
        page_plot.yaxis.set_label_coords(-.11, .5)

        page_plot.add_patch(Rectangle((self.page_left, self.page_bottom),
                                      (self.page_right-self.page_left),
                                      (self.page_top-self.page_bottom),
                                      fill=None, edgecolor='b', alpha=1))

        for index, line_dict in self.lines_dict.items():
            for line_index in line_dict.keys():
                if len(self.lines_dict) > 1 and len(self.lines_dict) < 3:
                    if index == 0:
                        xmax_value = self.center - .005
                        xmin_value = 0
                    elif index == 1:
                        xmax_value = 1
                        xmin_value = self.center - .005

                elif len(self.lines_dict) > 2:
                    if index == 0:
                        xmax_value = self.third_first - .005
                        xmin_value = 0
                    elif index == 1:
                        xmax_value = self.third_second - .005
                        xmin_value = self.third_first - .005
                    elif index == 2:
                        xmax_value = 1
                        xmin_value = self.third_second - .005

                else:
                    xmin_value = 0
                    xmax_value = 1

                page_plot.axhline(y=line_index, xmin=xmin_value, xmax=xmax_value)

        return page_plot

    def intantiate_columns(self):
        """Plot words on page/figure."""

        for dictionary in self.lines_dict.values():
            xmlColumnOperator.xmlColumnOperator(dictionary, self.page, self.page_plot,
                                                self.page_left, self.page_right, self.center,
                                                self.left_column_start, self.third_first_start,
                                                self.third_second_start, self.search_key_center,
                                                self.search_key_thirds)

            for word in self.words_excluded:
                xmlWordOperators.xmlWordOperators(self.page_plot, word, 'k')
