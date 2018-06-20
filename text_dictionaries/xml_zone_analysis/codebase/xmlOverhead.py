"""Top-level project Main function."""

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

        start_time = RunTimeData.read_pickle_start(self.zones_dictionary)
        with open(self.zones_dictionary, 'rb') as object_in:
            manual_zones_dictionary = pickle.load(object_in)

        with open(self.data_dictionary, 'rb') as object_in:
            manual_data_dictionary = pickle.load(object_in)

        page_data = manual_data_dictionary[0]
        line_data = manual_data_dictionary[1]
        manual_zones_dictionary_input = manual_zones_dictionary[0]
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
