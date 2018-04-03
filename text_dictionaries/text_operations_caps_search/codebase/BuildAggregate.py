"""Construct aggregate text blob from multiple manuals."""

import os

def build_aggregate(lower_bound, upper_bound):
    """Construct aggregate text blob from multiple manuals."""

    year_list = ['/Users/alextruesdale/Documents/moodys_code/WIP/text_dictionaries/text_output/industrials19{}.txt'.format(year)
                 for year in range(lower_bound, upper_bound)]

    if os.path.exists('working_directory/decade_aggregate.txt'):
        os.remove('working_directory/decade_aggregate.txt')

    for append_file in year_list:
        with open(append_file, 'r') as append_file:
            with open('working_directory/decade_aggregate.txt', 'a') as decade_aggregate:
                file_read = append_file.read()
                decade_aggregate.write(file_read)

    with open('working_directory/decade_aggregate.txt', 'r') as decade_aggregate:
        working_file = decade_aggregate.read()

    return working_file
