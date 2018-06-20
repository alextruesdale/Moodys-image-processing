import sys
import time
import datetime

def starting_print_statement():
    """Initialising print statement at beginning of Run Time."""

    start_time = [time.time(), datetime.datetime.now()]
    print('Start Time:', start_time[1].strftime("%H:%M:%S"))
    time_elapsed = time.time()

    return (start_time, time_elapsed)

def interim_print_statement(file, start_time, time_elapsed):
    """Recurring print statement throughout Job."""

    if datetime.datetime.now().strftime("%H:%M:%S") != start_time[1].strftime("%H:%M:%S"):
        current_job_time = time.time() - time_elapsed
        print('Current Time:', datetime.datetime.now().strftime("%H:%M:%S"))
        print('Previous Year Manual Duration:', round(current_job_time / 60, 2), 'minutes')

    time_elapsed = time.time()
    print('Active File:', file)
    return time_elapsed

def read_pickle_start(in_file):
    """Display read time data for pickle in-file reads."""

    start_time = time.time()
    print('Reading file:', in_file)
    return start_time

def read_pickle_end(start_time, in_file):
    """Display read time data for pickle in-file reads."""

    time_elapsed = time.time() - start_time
    print('File read:', in_file)
    print('Read time:', round(time_elapsed / 60, 2), 'minutes')

def time_elapsed_placeholder(start_time):
    """Create placeholder for timestamps while searching for starting file."""

    time_elapsed = time.time() - start_time[0]
    return time_elapsed

def concluding_print_statement(start_time, time_elapsed):
    """Concluding print statement at end of Run Time."""

    current_job_time = time.time() - time_elapsed
    elapsed_time = round(time.time() - start_time[0], 2)
    print('Previous Year Manual Duration:', round(current_job_time / 60, 2), 'minutes')
    print('Total Duration:', str(round(elapsed_time/60, 2)) + ' minutes')
