"""Plot new table zone to check for errors."""

import os
import sys

sys.path.append('../../xml_build_charts_zones/codebase')
import xmlPlottingParent

class xmlModifiedTablesPlot(object):

    def __init__(self, year, charts_out_path, modified_pages, page_data):

        self.year = year
        self.charts_out_path = charts_out_path
        self.modified_pages = [modified_pages, []]
        self.page_data = page_data
        self.plot_new_table_zone()

    def plot_new_table_zone(self):
        """Plot new table zone to check for errors."""

        owd = os.getcwd()
        xmlPlottingParent.xmlPlottingParent(self.year, self.charts_out_path,
                                            self.modified_pages, self.page_data, True)

        os.chdir(owd)
