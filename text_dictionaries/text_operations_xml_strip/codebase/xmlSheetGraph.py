"""Construct word map graph booklet and assemble section gutter information"""

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages
import xmlStaticOperators
import xmlPageData
import xmlChartPage
import xmlColumnChart
import re
import os

class xmlSheetGraph(object):

    def __init__(self, file_path, xml_data):

        self.page_data_dictionary = xml_data.page_data_dictionary
        self.file_path = file_path
        self.year = self.identify_year()
        self.section_dictionary = self.chart_page_by_page_class()

    def identify_year(self):
        """Extract year from file path."""

        year = re.search(r'.*Industrials_(\d{4}).*', self.file_path).group(1)
        return year

    def chart_page_by_page_class(self):
        """Initialise class containing page data."""

        save_path = '../text_output/sheet_directory/'
        save_name = '{}_plots.pdf'.format(self.year)
        company_output_destination = 'company_names.txt'
        xmlStaticOperators.clear_destination(save_path + save_name)
        xmlStaticOperators.clear_destination(save_path + company_output_destination)

        os.chdir(save_path)
        section_dictionary_center = {}
        section_dictionary_thirds = {}
        for i, (page, data) in enumerate(self.page_data_dictionary.items()):
            page_data = xmlPageData.xmlPageData(page, data)
            self.page_data_dictionary[page] = page_data

            section_dictionary_center.update({i: [page, page_data.gutter_count_center]})
            section_dictionary_thirds.update({i: [page, page_data.gutter_count_thirds]})

        xml_column_chart_center = xmlColumnChart.xmlColumnChart(section_dictionary_center, 'center')
        xml_column_chart_thirds = xmlColumnChart.xmlColumnChart(section_dictionary_thirds, 'thirds')

        print(xml_column_chart_center.section_list)
        print(xml_column_chart_thirds.section_list)

        with PdfPages(save_name) as pdf:
            for i, (page, data) in enumerate(self.page_data_dictionary.items()):
                i = 1000 + i
                xmlChartPage.xmlChartPage(i, data, xml_column_chart_center, xml_column_chart_thirds)

                pdf.savefig()
                plt.close()
