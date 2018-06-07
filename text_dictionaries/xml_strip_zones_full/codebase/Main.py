"""Top-level project Main function."""

import sys
import pickle
import xmlStripper

sys.path.append('../../../runtime_data/')
import RunTimeData

def main():
    """Top-level project Main function."""

    def construct_paths(lower_bound, upper_bound):
        """Construct list of file paths for operation."""

        file_dict = {int('19' + str(year)): [
                     '/Volumes/SamsungT5/moodys_files/raw_xml/Industrials_19{}_raw_image.xml'.format(year),
                     '../../text_output/pickle_objects/full_objects_zones/Industrials_19{}_zones.file'.format(year)
                     ] for year in range(lower_bound, upper_bound)}

        return file_dict

    starting_data = RunTimeData.starting_print_statement()
    start_time = starting_data[0]
    time_elapsed = starting_data[1]

    # try:
    file_dict = construct_paths(29, 30)
    for file_path_list in file_dict.values():
        in_file = file_path_list[0]
        pickle_out_file = file_path_list[1]

        time_elapsed = RunTimeData.interim_print_statement(in_file, start_time, time_elapsed)
        with open(in_file, 'r') as file_open:
            working_file = file_open.read()

        xml_data = xmlStripper.xmlStripper(in_file, working_file)
        pickle_data = (xml_data.zone_data_dictionary, xml_data.dictionary_length)

        with open(pickle_out_file, 'wb') as file_out:
            pickle.dump(pickle_data, file_out, pickle.HIGHEST_PROTOCOL)

        del xml_data

    RunTimeData.concluding_print_statement(start_time, time_elapsed)

if __name__ == "__main__":
    main()
