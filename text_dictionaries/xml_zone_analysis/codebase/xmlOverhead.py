"""Overhead module to contain sub-modules and extract specific attributes therein."""

import sys
import pickle
import time
import xmlStaticOperators
import xmlTableIdentifier
import xmlModifiedTablesPlot

sys.path.append('../../xml_firm_search/codebase')
import xmlPageData

sys.path.append('../../../runtime_data/')
import RunTimeData

class xmlOverhead(object):

    """
    Wrapper for modules/classes one level deeper.
    Extracts basic data from those modules as meta data for the entire programme.

    Attributes:

    data_dictionary: path to data dictionary pickle file.
    zones_dictionary: path to zones dictionary pickle file.
    data_out_path: out path for saved data.
    charts_out_path: out path for saved charts.
    year: trailing two digits of manual year (i.e. 45 for 1945).

    pickle_data: returned data from read_pickle_files()
        page_data: page data object stored in pickle file.
        line_data: line data object stored in pickle file.
        manual_zones_dictionary_input: zones dictionary object stored in pickle file.

    table_aggregate_data: returned data from instantiate_table_identifier()
        manual_fullwidth_table_count: count of full-width tables in manual.
        manual_fullwidth_ideal_table_count: count of clean full-width tables in manual.
        table_keys_aggregate: list of table keys in manual.
        modified_pages: dictionary with modified tables and zone-data objects.
    """

    def __init__(self, data_dictionary, zones_dictionary, data_out_path, charts_out_path, year):

        self.data_dictionary = data_dictionary
        self.zones_dictionary = zones_dictionary
        self.data_out_path = data_out_path
        self.charts_out_path = charts_out_path
        self.year = year

        self.pickle_data = self.read_pickle_files()
        self.page_data = self.pickle_data[0]
        self.line_data = self.pickle_data[1]
        self.manual_zones_dictionary_input = self.pickle_data[2]

        self.clear_output_paths()

        self.table_aggregate_data = self.instantiate_table_identifier()
        self.manual_fullwidth_table_count = self.table_aggregate_data[0]
        self.manual_fullwidth_ideal_table_count = self.table_aggregate_data[1]
        self.table_keys_aggregate = self.table_aggregate_data[2]
        self.modified_pages = self.table_aggregate_data[3]
        self.instantiate_modified_tables_plotter()

    def read_pickle_files(self):
        """Read pickle files into memory."""

        # print start time of pickle file read.
        start_time = RunTimeData.read_pickle_start(self.zones_dictionary)

        # open pickled files and assign data to temporary objects.
        with open(self.zones_dictionary, 'rb') as object_in:
            manual_zones_dictionary = pickle.load(object_in)

        with open(self.data_dictionary, 'rb') as object_in:
            manual_data_dictionary = pickle.load(object_in)

        # define objects to be returned and passed on.
        page_data = manual_data_dictionary[0]
        line_data = manual_data_dictionary[1]
        manual_zones_dictionary_input = manual_zones_dictionary[0]

        # print end time of pickle file read.
        RunTimeData.read_pickle_end(start_time, self.zones_dictionary)

        return (page_data, line_data, manual_zones_dictionary_input)

    def clear_output_paths(self):
        """Clear output paths for data and charts to be saved."""

        xmlStaticOperators.clear_destination(self.data_out_path)
        xmlStaticOperators.clear_destination(self.charts_out_path)

    def instantiate_table_identifier(self):
        """Trigger xmlTableIdentifier class."""

        table_identifier_out = xmlTableIdentifier.xmlTableIdentifier(self.year, self.data_out_path,
                                                                     self.manual_zones_dictionary_input,
                                                                     self.page_data, self.line_data)

        # access aggregate data to be fed out to meta data counters.
        table_aggregate_data = table_identifier_out.table_aggregate_data
        manual_fullwidth_table_count = table_aggregate_data[0]
        manual_fullwidth_ideal_table_count = table_aggregate_data[1]
        table_keys_aggregate = table_aggregate_data[2]
        modified_pages = table_aggregate_data[3]

        return (manual_fullwidth_table_count, manual_fullwidth_ideal_table_count,
                table_keys_aggregate, modified_pages)

    def instantiate_modified_tables_plotter(self):
        """Trigger xmlModifiedTablesPlot class."""

        print('plotting charts...')
        xmlModifiedTablesPlot.xmlModifiedTablesPlot(self.year, self.charts_out_path,
                                                    self.modified_pages, self.page_data)
