"""Parent function for sheet plotting."""

import os
import xmlPlotPage
from operator import itemgetter
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class xmlPlottingParent(object):

    def __init__(self, year, charts_out_file, manual_zones_dictionary, page_data_dictionary, manual_operate_key_overwrite):

        self.year = '19' + year
        self.out_file = charts_out_file
        self.manual_zones_dictionary = manual_zones_dictionary[0]
        self.page_data = page_data_dictionary
        self.manual_operate_key_overwrite = manual_operate_key_overwrite

        self.create_chart_wrapper()

    @staticmethod
    def manual_begin_end(year, page_index):
        """define beginning and endpoints of manual in terms of areas to search."""

        manual_begin_end_dict = {
            '1920': [[-1, False], [133, True], [1513, False]],
            '1921': [[-1, False], [158, True], [1751, False]],
            '1922': [[-1, False], [193, True], [2077, False]],
            '1923': [[-1, False], [159, True], [2414, False]],
            '1924': [[-1, False], [310, True], [2878, False]],
            '1925': [[-1, False], [225, True], [2405, False]],
            '1926': [[-1, False], [270, True], [2665, False]],
            '1927': [[-1, False], [306, True], [3057, False]],
            '1928': [[-1, False], [348, True], [3425, False]],
            '1929': [[-1, False], [391, True], [3485, False]]
        }

        difference_list = sorted([[item, page_index - item[0]] for item in
                                  manual_begin_end_dict[year] if page_index - item[0] > 0],
                                  key=itemgetter(1))

        begin_end_value = difference_list[0][0][1]
        return begin_end_value

    def create_chart_wrapper(self):
        """"""

        split_path = self.out_file.split('/')
        save_path = '/'.join(split_path[:-1])
        save_name = split_path[-1]
        os.chdir(save_path)

        with PdfPages(save_name) as pdf:
            for i, (page, data) in enumerate(self.manual_zones_dictionary.items()):
                manual_operate_key = xmlPlottingParent.manual_begin_end(self.year, i)

                if manual_operate_key or self.manual_operate_key_overwrite:
                    if page in self.page_data.keys():
                        xmlPlotPage.xmlPlotPage(page, data, self.page_data[page])

                        pdf.savefig()
                        plt.close()
