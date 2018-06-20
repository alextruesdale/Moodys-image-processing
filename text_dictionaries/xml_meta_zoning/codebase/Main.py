"""Top-level project Main function."""

import sys
import pickle
from OperatorContainer import OperatorContainer

sys.path.append('../../../runtime_data/')
import RunTimeData

def main():
    """Top-level project Main function."""

    def construct_paths(lower_bound, upper_bound):
        """Construct list of file paths for operation."""

        file_dict = {int('19' + str(year)): [
                     '../../text_output/pickle_objects/full_objects_words/Industrials_19{}_dictionary.file'.format(year),
                     '../../text_output/xml_word_charts_meta/19{}_plots.pdf'.format(year),
                     str(year)] for year in range(lower_bound, upper_bound)}

        return file_dict

    starting_data = RunTimeData.starting_print_statement()
    start_time = starting_data[0]
    time_elapsed = starting_data[1]

    file_dict = construct_paths(40, 42)
    for file_path_list in file_dict.values():
        in_file = file_path_list[0]
        out_file = file_path_list[1]
        year = file_path_list[2]

        time_elapsed = time_elapsed = RunTimeData.interim_print_statement(in_file, start_time, time_elapsed)
        pickle_start_time = RunTimeData.read_pickle_start(in_file)
        with open(in_file, 'rb') as object_in:
            xml_data = pickle.load(object_in)
            RunTimeData.read_pickle_end(pickle_start_time, in_file)

        page_data_dictionary = xml_data[0]
        OperatorContainer(year, page_data_dictionary, out_file)


    RunTimeData.concluding_print_statement(start_time, time_elapsed)

if __name__ == "__main__":
    main()
