"""Top-level project Main function."""

from ColumnCropper import ColumnCropper
import ImageReader
import RunTimeData
import ColumnWindowFinder

import sys
sys.path.append('../../runtime_data/')
import RunTimeData

def main():
    """Read file directory images and the run the Image Operator aggregate function."""

    starting_data = RunTimeData.starting_print_statement()
    start_time = starting_data[0]
    time_elapsed = starting_data[1]

    files = ImageReader.read_files('include', 'output')
    total_files = 0
    year_out = ''
    for page_index, file_path in enumerate(files):

        year = file_path[-17:-13]
        if ColumnWindowFinder.run_filter(page_index, year):
            file_operate = ColumnCropper(file_path, page_index, start_time, time_elapsed)
            time_elapsed = file_operate.time_elapsed
            total_files += 1

    RunTimeData.concluding_print_statement(start_time, time_elapsed)
    print(total_files)

if __name__ == "__main__":
    main()
