"""Top-level project Main Module."""

from FileOperations import file_operations

import sys
sys.path.append('../../../runtime_data/')
import RunTimeData

def main():
    """Top-level project Main function."""

    def construct_paths(lower_bound, upper_bound):
        """Construct list of file paths for operations (input and output file paths)."""

        file_dict = {str(file_id).zfill(2): [
                     '../from_summit/ConfZones0{}'.format(str(file_id).zfill(2)),
                     '../from_summit/TextZones0{}'.format(str(file_id).zfill(2))]
                     for file_id in range(lower_bound, upper_bound)}

        return file_dict

    # trigger console printing function and define variables for mid-runtime print statements.
    starting_data = RunTimeData.starting_print_statement()
    start_time = starting_data[0]
    time_elapsed = starting_data[1]

    # construct list of input paths for 'ConfZones files'.
    # arguments represent the range of inputs (i.e. 0, 5 = ConfZones000
    # through ConfZones004).

    file_dict = construct_paths(0, 1)

    # trigger file_operations class to read and combine zone files and output as objects.
    zone_data = file_operations(file_dict)

    # print concluding job console statement with summarising data.
    RunTimeData.concluding_print_statement(start_time, time_elapsed)


if __name__ == '__main__':
    main()
