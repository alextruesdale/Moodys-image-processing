"""Top-level project Main function."""

import sys
import pickle
import xmlSheetSearch
import xmlStaticOperators

sys.path.append('../../../runtime_data/')
import RunTimeData

def main():
    """Top-level project Main function."""

    def construct_paths(lower_bound, upper_bound):
        """Construct list of file paths for operation."""

        file_dict = {int('19' + str(year)): [
                     '../../text_output/pickle_objects/full_objects_words/Industrials_19{}_dictionary.file'.format(year),
                     '../../text_output/pickle_objects/firm_location_objects/Industrials_19{}_firms.file'.format(year),
                     str(year)] for year in range(lower_bound, upper_bound)}

        return file_dict

    starting_data = RunTimeData.starting_print_statement()
    start_time = starting_data[0]
    time_elapsed = starting_data[1]

    # try:
    file_dict = construct_paths(40, 42)
    for file_path_list in file_dict.values():
        in_file = file_path_list[0]
        firms_out_file = file_path_list[1]
        year = file_path_list[2]
        outfiles = {}

        time_elapsed = time_elapsed = RunTimeData.interim_print_statement(firms_out_file, start_time, time_elapsed)
        with open(in_file, 'rb') as object_in:
            xml_data = pickle.load(object_in)

        xml_sheet = xmlSheetSearch.xmlSheetSearch(in_file, xml_data)
        firm_data = xml_sheet.location_data
        outfiles.update({firms_out_file: firm_data})

        page_data_outfile = '../../text_output/pickle_objects/page_data_objects/Industrials_19{}_data_dictionary.file'.format(year)
        page_data_dictionary = xml_sheet.page_data_dictionary
        page_line_data = xml_sheet.line_data
        outfiles.update({page_data_outfile: [page_data_dictionary, page_line_data]})

        for out_file, data in outfiles.items():
            xmlStaticOperators.clear_destination(out_file)
            with open(out_file, 'wb') as file_out:
                pickle.dump(data, file_out, pickle.HIGHEST_PROTOCOL)

    RunTimeData.concluding_print_statement(start_time, time_elapsed)

if __name__ == "__main__":
    main()
