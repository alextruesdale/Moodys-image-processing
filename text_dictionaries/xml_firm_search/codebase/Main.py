"""Top-level project Main function."""

import sys
import time
import datetime
import pickle
import logging
import xmlSheetSearch
import xmlStaticOperators

logging.basicConfig(filename='RuntimeErrors.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    """Top-level project Main function."""

    def construct_paths(lower_bound, upper_bound):
        """Construct list of file paths for operation."""

        file_dict = {int('19' + str(year)): [
                     '../../text_output/pickle_objects/full_objects_words/Industrials_19{}_dictionary.file'.format(year),
                     '../../text_output/pickle_objects/firm_location_objects/Industrials_19{}_firms.file'.format(year),
                     str(year)] for year in range(lower_bound, upper_bound)}

        return file_dict

    start_time = [time.time(), datetime.datetime.now()]
    print('Start Time:', start_time[1].strftime("%H:%M:%S"))
    time_elapsed = time.time()

    # try:
    file_dict = construct_paths(20, 30)
    for file_path_list in file_dict.values():
        in_file = file_path_list[0]
        firms_out_file = file_path_list[1]
        year = file_path_list[2]
        outfiles = {}

        if datetime.datetime.now().strftime("%H:%M:%S") != start_time[1].strftime("%H:%M:%S"):
            current_job_time = time.time() - time_elapsed
            print('Current Time:', datetime.datetime.now().strftime("%H:%M:%S"))
            print('Previous Year Manual Duration:', round(current_job_time / 60, 2), 'minutes')

        time_elapsed = time.time()
        print('Active File:', in_file)

        with open(in_file, 'rb') as object_in:
            xml_data = pickle.load(object_in)

        xml_sheet = xmlSheetSearch.xmlSheetSearch(in_file, xml_data)
        # firm_data = xml_sheet.location_data
        # outfiles.update({firms_out_file: firm_data})
        #
        # page_data_outfile = '../../text_output/pickle_objects/page_data_objects/Industrials_19{}_data_dictionary.file'.format(year)
        # page_data_dictionary = xml_sheet.page_data_dictionary
        # page_line_data = xml_sheet.line_data
        # outfiles.update({page_data_outfile: [page_data_dictionary, page_line_data]})
        #
        # for out_file, data in outfiles.items():
        #     xmlStaticOperators.clear_destination(out_file)
        #     with open(out_file, 'wb') as file_out:
        #         pickle.dump(data, file_out, pickle.HIGHEST_PROTOCOL)

    # except Exception as e:
    #     logger.error('Error Message: ' + str(e), exc_info=True)

    current_job_time = time.time() - time_elapsed
    elapsed_time = round(time.time() - start_time[0], 2)
    print('Previous Year Manual Duration:', round(current_job_time / 60, 2), 'minutes')
    print('Total Duration:', str(round(elapsed_time/60, 2)) + ' minutes')

if __name__ == "__main__":
    main()
