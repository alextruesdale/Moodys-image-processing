"""Top-level project Main function."""

import time
import datetime
import xmlOverhead
import xmlStaticOperators
from collections import Counter

def main():
    """Top-level project Main function."""

    def construct_paths(lower_bound, upper_bound):
        """Construct list of file paths for operation."""

        file_dict = {int('19' + str(year)): [
                     '../../text_output/pickle_objects/page_data_objects/Industrials_19{}_data_dictionary.file'.format(year),
                     '../../text_output/pickle_objects/full_objects_zones/Industrials_19{}_zones.file'.format(year),
                     '../../text_output/xml_zone_data/19{}_data'.format(year),
                     '../../text_output/xml_zone_data/19{}_data/19{}_plots.pdf'.format(year, year), str(year)]
                     for year in range(lower_bound, upper_bound)}

        return file_dict

    start_time = [time.time(), datetime.datetime.now()]
    print('Start Time:', start_time[1].strftime("%H:%M:%S"))
    time_elapsed = time.time()

    decade_fullwidth_table_count = 0
    decade_fullwidth_ideal_table_count = 0
    table_keys_insgesammt = Counter()

    file_dict = construct_paths(21, 23)
    for file_path_list in file_dict.values():
        data_dictionary = file_path_list[0]
        zones_dictionary = file_path_list[1]
        data_out_path = file_path_list[2]
        charts_out_path = file_path_list[3]
        year = file_path_list[4]

        if datetime.datetime.now().strftime("%H:%M:%S") != start_time[1].strftime("%H:%M:%S"):
            current_job_time = time.time() - time_elapsed
            print('Current Time:', datetime.datetime.now().strftime("%H:%M:%S"))
            print('Previous Year Manual Duration:', round(current_job_time / 60, 2), 'minutes')

        time_elapsed = time.time()
        print('Active File:', zones_dictionary)

        xml_year_data = xmlOverhead.xmlOverhead(data_dictionary, zones_dictionary,
                                                data_out_path, charts_out_path, year)

        decade_fullwidth_table_count += xml_year_data.manual_fullwidth_table_count
        decade_fullwidth_ideal_table_count += xml_year_data.manual_fullwidth_ideal_table_count
        for key in xml_year_data.table_keys_aggregate:
            table_keys_insgesammt[key] += 1

        del xml_year_data

    table_keys_insgesammt_path = '../../text_output/xml_zone_data/1920_table_keys.txt'
    xmlStaticOperators.clear_destination(table_keys_insgesammt_path)
    for count in table_keys_insgesammt.most_common(1000):
        count_out = str(count[1]) + '  |  ' + count[0]
        with open(table_keys_insgesammt_path, 'a') as out_file:
            out_file.write(count_out)
            out_file.write('\n')

    current_job_time = time.time() - time_elapsed
    elapsed_time = round(time.time() - start_time[0], 2)
    print('Previous Year Manual Duration:', round(current_job_time / 60, 2), 'minutes')
    print('Total Duration:', str(round(elapsed_time / 60, 2)) + ' minutes')


if __name__ == "__main__":
    main()
