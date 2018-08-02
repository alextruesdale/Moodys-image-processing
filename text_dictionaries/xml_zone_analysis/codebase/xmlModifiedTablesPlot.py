"""Plot new table zone to check for errors."""

import os
import sys

sys.path.append('../../xml_build_charts_zones/codebase')
import xmlPlottingParent

class xmlModifiedTablesPlot(object):

    """
    Access chart building module and print modified sheets to PDF booklet.

    Attributes:

    year: year of manual.
    charts_out_path: path to print PDF to.
    modified_pages: incoming dict. of modified pages and zones (configured to match
                    charting module requirements).

    page_data: page data dictionary for manual.
    """

    def __init__(self, year, charts_out_path, modified_pages, page_data):

        self.year = year
        self.charts_out_path = charts_out_path
        self.modified_pages = [modified_pages, []]
        self.page_data = page_data
        self.plot_new_table_zone()

    def plot_new_table_zone(self):
        """Plot new table zone to check for errors."""

        # store current working directory.
        owd = os.getcwd()

        # trigger plotting class and its subclasses.
        xmlPlottingParent.xmlPlottingParent(self.year, self.charts_out_path,
                                            self.modified_pages, self.page_data, True)

        # return to previous working directory (xmlPlottingParent changes dir.)
        os.chdir(owd)
