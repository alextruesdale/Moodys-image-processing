"""Top-level project Main function."""

import sys
import time
import logging
import BuildAggregate
import PreliminaryParsing
import BuildDictionariesCaps

logging.basicConfig(filename='RuntimeErrors.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)

run_type = sys.argv[1]
def main(run_type):
    """Top-level project Main function."""

    start_time = time.time()

    try:
        if run_type == 'build':
            working_file = BuildAggregate.build_aggregate(30, 31)
            highlevel_data = PreliminaryParsing.PreliminaryParsing(working_file)

        elif run_type == 'run':
            uppercase_dictionaries = BuildDictionariesCaps.CapsDictionaries()

    except Exception as e:
        logger.error('Error Message: ' + str(e), exc_info=True)

    elapsed_time = round(time.time() - start_time, 2)
    print('Duration:', str(elapsed_time) + ' seconds')


if __name__ == "__main__":
    main(run_type)
