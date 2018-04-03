"""Top-level project Main function."""

import sys
import time
import logging
import xmlStripper
import xmlSheetGraph

logging.basicConfig(filename='RuntimeErrors.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    """Top-level project Main function."""

    def construct_paths(lower_bound, upper_bound):
        """Construct list of file paths for operation."""

        file_list = ['../text_output/xml_directory/Industrials_19{}_raw_image.xml'.format(year)
                     for year in range(lower_bound, upper_bound)]

        return file_list

    start_time = time.time()

    # try:
    file_list = construct_paths(30, 31)
    for file_path in file_list:
        print(file_path)
        with open(file_path, 'r') as file_open:
            working_file = file_open.read()

    xml_data = xmlStripper.xmlStripper(file_path, working_file)
    xml_sheet_graphs = xmlSheetGraph.xmlSheetGraph(file_path, xml_data)

    # except Exception as e:
    #     logger.error('Error Message: ' + str(e), exc_info=True)

    elapsed_time = round(time.time() - start_time, 2)
    print('Duration:', str(elapsed_time) + ' seconds')


if __name__ == "__main__":
    main()
