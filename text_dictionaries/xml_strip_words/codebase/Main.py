"""Top-level project Main function."""

import sys
import time
import datetime
import pickle
import logging
import xmlStripper

logging.basicConfig(filename='RuntimeErrors.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    """Top-level project Main function."""

    def construct_paths(lower_bound, upper_bound):
        """Construct list of file paths for operation."""

        file_dict = {int('19' + str(year)): [
                     '/Volumes/SamsungT5/Dropbox/moodys_files/raw_xml/Industrials_19{}_raw_image.xml'.format(year),
                     '../../text_output/pickle_objects/Industrials_19{}_dictionary.file'.format(year)
                     ] for year in range(lower_bound, upper_bound)}

        return file_dict

    start_time = [time.time(), datetime.datetime.now()]
    print('Start Time:', start_time[1].strftime("%H:%M:%S"))
    time_elapsed = time.time()

    # try:
    file_dict = construct_paths(30, 40)
    for file_path_list in file_dict.values():
        in_file = file_path_list[0]
        pickle_out_file = file_path_list[1]

        if datetime.datetime.now().strftime("%H:%M:%S") != start_time[1].strftime("%H:%M:%S"):
            current_job_time = time.time() - time_elapsed
            print('Current Time:', datetime.datetime.now().strftime("%H:%M:%S"))
            print('Previous Year Manual Duration:', round(current_job_time / 60, 2), 'minutes')

        time_elapsed = time.time()
        print('Active File:', in_file)

        with open(in_file, 'r') as file_open:
            working_file = file_open.read()

        xml_data = xmlStripper.xmlStripper(in_file, working_file)
        pickle_data = (xml_data.page_data_dictionary, xml_data.dictionary_length)

        with open(pickle_out_file, 'wb') as file_out:
            pickle.dump(pickle_data, file_out, pickle.HIGHEST_PROTOCOL)

    # except Exception as e:
    #     logger.error('Error Message: ' + str(e), exc_info=True)

    current_job_time = time.time() - time_elapsed
    elapsed_time = round(time.time() - start_time[0], 2)
    print('Previous Year Manual Duration:', round(current_job_time / 60, 2), 'minutes')
    print('Total Duration:', str(round(elapsed_time/60, 2)) + ' minutes')

if __name__ == "__main__":
    main()
