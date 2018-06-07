"""Top-level project Main function."""

import sys
import pickle
import xmlPlottingParent
import xmlStaticOperators

sys.path.append('../../xml_firm_search/codebase')
import xmlPageData

sys.path.append('../../../runtime_data/')
import RunTimeData

def main():
    """Top-level project Main function."""

    def construct_paths(lower_bound, upper_bound):
        """Construct list of file paths for operation."""

        file_dict = {int('19' + str(year)): [
                     '../../text_output/pickle_objects/page_data_objects/Industrials_19{}_data_dictionary.file'.format(year),
                     '../../text_output/pickle_objects/full_objects_zones/Industrials_19{}_zones.file'.format(year),
                     '../../text_output/xml_zones_charts/19{}_plots.pdf'.format(year), str(year)]
                     for year in range(lower_bound, upper_bound)}

        return file_dict

    starting_data = RunTimeData.starting_print_statement()
    start_time = starting_data[0]
    time_elapsed = starting_data[1]

    # try:
    file_dict = construct_paths(21, 30)
    for file_path_list in file_dict.values():
        data_dictionary = file_path_list[0]
        zones_dictionary = file_path_list[1]
        charts_out_file = file_path_list[2]
        year = file_path_list[3]

        time_elapsed = time_elapsed = RunTimeData.interim_print_statement(charts_out_file, start_time, time_elapsed)
        with open(zones_dictionary, 'rb') as object_in:
            manual_zones_dictionary = pickle.load(object_in)

        with open(data_dictionary, 'rb') as object_in:
            manual_data_dictionary = pickle.load(object_in)

        page_data_dictionary = manual_data_dictionary[0]
        xmlStaticOperators.clear_destination(charts_out_file)
        xmlPlottingParent.xmlPlottingParent(year, charts_out_file, manual_zones_dictionary,
                                            page_data_dictionary, False)

    RunTimeData.concluding_print_statement(start_time, time_elapsed)

if __name__ == "__main__":
    main()
