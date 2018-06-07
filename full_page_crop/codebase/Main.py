"""Top-level project Main function."""

import ImageReader
from ImageOperator import ImageOperator
import RunTimeData

import sys
sys.path.append('../../runtime_data/')
import RunTimeData

def main():
    """Read file directory images and the run the Image Operator aggregate function."""

    starting_data = RunTimeData.starting_print_statement()
    start_time = starting_data[0]
    time_elapsed = starting_data[1]

    files = ImageReader.file_read_operate('exclude', 'output')
    total_files = 0
    year_out = ''
    for page_index, file_path in enumerate(files):

        year = file_path[-17:-13]
        file_operate = ImageOperator(file_path, year, page_index, start_time, time_elapsed)
        time_elapsed = file_operate.time_elapsed
        total_files += 1
        year_out = year

    RunTimeData.concluding_print_statement(start_time, time_elapsed)
    print(total_files)

if __name__ == "__main__":
    main()
