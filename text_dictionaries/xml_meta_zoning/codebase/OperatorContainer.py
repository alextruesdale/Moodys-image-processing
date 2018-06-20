"""Container class for workflow operations."""

import sys
import os
from LineSearch import LineSearch
from PlotPage import PlotPage
from operator import itemgetter
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

sys.path.append('../../xml_firm_search/codebase')
from xmlPageData import xmlPageData

class OperatorContainer(object):

    def __init__(self, year, page_data_dictionary, out_file):

        self.year = '19' + year
        self.page_data_dictionary = page_data_dictionary
        self.out_file = out_file
        self.page_data_dictionary_update()
        self.line_definer_plot()

    @staticmethod
    def manual_begin_end(year, page_index):
        """define beginning and endpoints of manual in terms of areas to search."""

        manual_begin_end_dict = {
            '1940': [[-1, False], [386, True], [3581, False]],
            '1941': [[-1, False], [329, True], [3466, False]]
        }

        single_column_page_dict = {
            '1940': [[-1, False], [386, True], [542, False], [1208, True], [1380, False],
                     [1740, True], [1837, False], [1896, True], [1916, False], [1995, True],
                     [2006, False], [2062, True],[2111, False], [2249, True], [2356, False],
                     [2393, True], [2408, False], [2425, True],[2450, False], [2597, True],
                     [2660, False], [2775, True], [2778, False], [2852, True],[2946, False],
                     [2991, True], [3581, False]],

            '1941': [[-1, False], [329, True], [608, False], [917, True], [999, False],
                     [1119, True], [1187, False], [1583, True], [1615, False], [1813, True],
                     [1847, False], [2031, True], [2068, False], [2140, True], [2308, False],
                     [2335, True], [2640, False], [2813, True], [3100, False], [3122, True],
                     [3165, False], [3191, True], [3466, False]]
        }

        difference_list_manual = sorted([[item, page_index - item[0]] for item in
                                          manual_begin_end_dict[year] if page_index - item[0] > 0],
                                          key=itemgetter(1))

        difference_list_page = sorted([[item, page_index - item[0]] for item in
                                        manual_begin_end_dict[year] if page_index - item[0] > 0],
                                        key=itemgetter(1))

        key_value_manual = difference_list_manual[0][0][1]
        key_value_manual = difference_list_page[0][0][1]

        run_key = False
        if key_value_manual and key_value_manual:
            run_key = True

        return run_key

    def page_data_dictionary_update(self):
        """Trigger page_data class and overwrite values in page_data_dictionary."""

        for i, (page, data) in enumerate(self.page_data_dictionary.items()):
            if OperatorContainer.manual_begin_end(self.year, i):
                page_data = xmlPageData(page, data)
                word_data = page_data.word_data
                page_bounds = page_data.page_bounds[0]
                self.page_data_dictionary[page] = [word_data, page_bounds]

    def line_definer_plot(self):
        """Instantiate page-level classes identifying page layout."""

        split_path = self.out_file.split('/')
        save_path = '/'.join(split_path[:-1])
        save_name = split_path[-1]
        os.chdir(save_path)

        with PdfPages(save_name) as pdf:
            for i, (page, data) in enumerate(self.page_data_dictionary.items()):
                if OperatorContainer.manual_begin_end(self.year, i):
                    line_search_out = LineSearch(page, data)
                    PlotPage(line_search_out)

                    pdf.savefig()
                    plt.close()
