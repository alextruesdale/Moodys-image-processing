"""Top-level project Main Module."""

import xmlOverhead
import xmlStaticOperators
from collections import Counter

import sys
sys.path.append('../../../runtime_data/')
import RunTimeData

def main():
    """Top-level project Main function."""

    def construct_paths(lower_bound, upper_bound):
        """Construct list of file paths for operations (input and output file paths)."""

        file_dict = {int('19' + str(year)): [
                     '../../text_output/pickle_objects/page_data_objects/Industrials_19{}_data_dictionary.file'.format(year),
                     '../../text_output/pickle_objects/full_objects_zones/Industrials_19{}_zones.file'.format(year),
                     '../../text_output/xml_zone_data/19{}_data'.format(year),
                     '../../text_output/xml_zone_data/19{}_data/19{}_plots.pdf'.format(year, year), str(year)]
                     for year in range(lower_bound, upper_bound)}

        return file_dict

    # trigger console printing function and define variables for mid-runtime print statements.
    starting_data = RunTimeData.starting_print_statement()
    start_time = starting_data[0]
    time_elapsed = starting_data[1]

    # define data counters that will be saved; summarising table data at manual-level.
    decade_fullwidth_table_count = 0
    decade_fullwidth_ideal_table_count = 0
    table_keys_insgesammt = Counter()

    # create dictionary of file paths; will be used to loop over multiple manuals.
    file_dict = construct_paths(20, 21)

    # loop over dictionary items (manuals) and trigger subordinate modules.
    for file_path_list in file_dict.values():
        data_dictionary = file_path_list[0]
        zones_dictionary = file_path_list[1]
        data_out_path = file_path_list[2]
        charts_out_path = file_path_list[3]
        year = file_path_list[4]

        # print job console data for each manual by year (item in dictionary).
        time_elapsed = RunTimeData.interim_print_statement(data_out_path, start_time, time_elapsed)

        # trigger overhead module (containing other modules); assign class output to object.
        xml_year_data = xmlOverhead.xmlOverhead(data_dictionary, zones_dictionary,
                                                data_out_path, charts_out_path, year)

        # access xml_year_data attributes and add them to above-defined counters.
        decade_fullwidth_table_count += xml_year_data.manual_fullwidth_table_count
        decade_fullwidth_ideal_table_count += xml_year_data.manual_fullwidth_ideal_table_count
        for key in xml_year_data.table_keys_aggregate:
            table_keys_insgesammt[key] += 1

        # delete xml_year_data class for memory management.
        del xml_year_data

    # define output path for .txt file containing counts of table keys.
    table_keys_insgesammt_path = '../../text_output/xml_zone_data/1920_table_keys.txt'

    # clear any files residing at this path location.
    xmlStaticOperators.clear_destination(table_keys_insgesammt_path)

    # take 1000 most common keys and save them to .txt out file.
    for count in table_keys_insgesammt.most_common(1000):
        count_out = str(count[1]) + '  |  ' + count[0]
        with open(table_keys_insgesammt_path, 'a') as out_file:
            out_file.write(count_out)
            out_file.write('\n')

    # print concluding job console statement with summarising data.
    RunTimeData.concluding_print_statement(start_time, time_elapsed)

if __name__ == "__main__":
    main()
