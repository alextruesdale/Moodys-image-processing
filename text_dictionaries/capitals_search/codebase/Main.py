"""Top-level project Main function."""

import sys
import BuildAggregate
import PreliminaryParsing
import BuildDictionariesCaps

sys.path.append('../../../runtime_data/')
import RunTimeData

run_type = sys.argv[1]
def main(run_type):
    """Top-level project Main function."""

    starting_data = RunTimeData.starting_print_statement()
    start_time = starting_data[0]
    time_elapsed = starting_data[1]

    if run_type == 'build':
        build_data = BuildAggregate.build_aggregate(30, 31, start_time, time_elapsed)
        working_file = build_data[0]
        time_elapsed = build_data[1]
        highlevel_data = PreliminaryParsing.PreliminaryParsing(working_file)

    elif run_type == 'run':
        time_elapsed = RunTimeData.interim_print_statement('running process: build capitals ditionaries.',
                                                           start_time, time_elapsed)

        uppercase_dictionaries = BuildDictionariesCaps.CapsDictionaries()

    RunTimeData.concluding_print_statement(start_time, time_elapsed)

if __name__ == "__main__":
    main(run_type)
