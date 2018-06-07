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
