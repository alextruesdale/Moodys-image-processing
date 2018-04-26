"""Top-level project Main function."""

import sys
import time
import datetime
import pickle
import logging
import xmlPlottingParent
import xmlStaticOperators

sys.path.append('../../text_operations_xml_firm_search/codebase')
import xmlPageData

logging.basicConfig(filename='RuntimeErrors.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    """Top-level project Main function."""

    def construct_paths(lower_bound, upper_bound):
        """Construct list of file paths for operation."""

        file_dict = {int('19' + str(year)): [
                     '../../text_output/pickle_objects/page_data_objects/Industrials_19{}_data_dictionary.file'.format(year),
                     '../../text_output/pickle_objects/firm_location_objects/Industrials_19{}_firms.file'.format(year),
                     '../../text_output/xml_words_charts/19{}_plots.pdf'.format(year), str(year)]
                     for year in range(lower_bound, upper_bound)}

        return file_dict

    start_time = [time.time(), datetime.datetime.now()]
    print('Start Time:', start_time[1].strftime("%H:%M:%S"))
    time_elapsed = time.time()

    # try:
    file_dict = construct_paths(28, 30)
    for file_path_list in file_dict.values():
        data_dictionary = file_path_list[0]
        firms = file_path_list[1]
        charts_out_file = file_path_list[2]
        year = file_path_list[3]

        if datetime.datetime.now().strftime("%H:%M:%S") != start_time[1].strftime("%H:%M:%S"):
            current_job_time = time.time() - time_elapsed
            print('Current Time:', datetime.datetime.now().strftime("%H:%M:%S"))
            print('Previous Year Manual Duration:', round(current_job_time / 60, 2), 'minutes')

        time_elapsed = time.time()
        print('Active File:', charts_out_file)

        with open(firms, 'rb') as object_in:
            manual_firms = pickle.load(object_in)

        with open(data_dictionary, 'rb') as object_in:
            manual_data_dictionary = pickle.load(object_in)

        page_data_dictionary = manual_data_dictionary[0]
        page_line_data = manual_data_dictionary[1]

        xmlStaticOperators.clear_destination(charts_out_file)
        xmlPlottingParent.xmlPlottingParent(year, charts_out_file, page_data_dictionary,
                                            page_line_data, manual_firms)

    # except Exception as e:
    #     logger.error('Error Message: ' + str(e), exc_info=True)

    current_job_time = time.time() - time_elapsed
    elapsed_time = round(time.time() - start_time[0], 2)
    print('Previous Year Manual Duration:', round(current_job_time / 60, 2), 'minutes')
    print('Total Duration:', str(round(elapsed_time/60, 2)) + ' minutes')


if __name__ == "__main__":
    main()
