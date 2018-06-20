"""Construct word map graph booklet and assemble section gutter information"""

import re
import os
from operator import itemgetter
import xmlStaticOperators
import xmlPageData
import xmlPageOperator
import xmlColumnChart
import xmlWordOperators

class xmlSheetSearch(object):

    def __init__(self, file_path, xml_data):

        self.page_data_dictionary = xml_data[0]
        self.dictionary_length = xml_data[1]
        self.file_path = file_path
        self.year = self.identify_year()

        self.section_dictionaries = self.define_page_section_dictionaries()
        self.section_dictionary_center = self.section_dictionaries[0]
        self.section_dictionary_thirds = self.section_dictionaries[1]

        self.page_graphs = self.chart_page_structure_graphs()
        self.xml_column_chart_center = self.page_graphs[0]
        self.xml_column_chart_thirds = self.page_graphs[1]

        self.firm_line_data = self.identify_firms_lines_locations_on_page()
        self.location_data = self.firm_line_data[0]
        self.line_data = self.firm_line_data[1]

    def identify_year(self):
        """Extract year from file path."""

        year = re.search(r'.*Industrials_(\d{4}).*', self.file_path).group(1)
        return year

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
            '1929': [[-1, False], [391, True], [3485, False]],
            '1940': [[-1, False], [386, True], [3581, False]],
            '1941': [[-1, False], [329, True], [3466, False]]
        }

        difference_list = sorted([[item, page_index - item[0]] for item in
                                  manual_begin_end_dict[year] if page_index - item[0] > 0],
                                  key=itemgetter(1))

        begin_end_value = difference_list[0][0][1]
        return begin_end_value

    def define_page_section_dictionaries(self):
        """Initialise class containing page data."""

        section_dictionary_center = {}
        section_dictionary_thirds = {}
        for i, (page, data) in enumerate(self.page_data_dictionary.items()):
            page_data = xmlPageData.xmlPageData(page, data)
            self.page_data_dictionary[page] = page_data

            section_dictionary_center.update({i: [page, page_data.gutter_count_center]})
            section_dictionary_thirds.update({i: [page, page_data.gutter_count_thirds]})

        return (section_dictionary_center, section_dictionary_thirds)

    def chart_page_structure_graphs(self):
        """"""

        xml_column_chart_center = xmlColumnChart.xmlColumnChart(self.section_dictionary_center, 'center', self.year)
        xml_column_chart_thirds = xmlColumnChart.xmlColumnChart(self.section_dictionary_thirds, 'thirds', self.year)

        return (xml_column_chart_center, xml_column_chart_thirds)

    def identify_firms_lines_locations_on_page(self):
        """"""

        file_path = '../../text_output/xml_firm_search_output/{}_company_names.txt'.format(self.year)
        xmlStaticOperators.clear_destination(file_path)

        firm_location_data = {}
        page_lines_data = {}
        for i, (page, data) in enumerate(self.page_data_dictionary.items()):
            manual_operate_key = xmlSheetSearch.manual_begin_end(self.year, i)

            if data.page_bounds[2] and manual_operate_key:
                page_operator_data = xmlPageOperator.xmlPageOperator(i, self.year, data, file_path,
                                                                     self.xml_column_chart_center,
                                                                     self.xml_column_chart_thirds)

                if len(page_operator_data.line_data_dict) > 0:
                    for key, value in page_operator_data.line_data_dict.items():
                        page_lines_data.update({key: value})

                if len(page_operator_data.page_break_dictionary_insgesamt) > 0:
                    for key, value in page_operator_data.page_break_dictionary_insgesamt.items():
                        firm_location_data.update({key: value})

        return (firm_location_data, page_lines_data)
