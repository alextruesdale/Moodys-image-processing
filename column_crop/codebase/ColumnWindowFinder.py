"""Identify if page is in single or multi-columns zone."""

from operator import itemgetter

def run_filter(page_index, year):
    """Determine whether or not to operate on incoming class file."""

    manual_begin_end_dict = {
        '1920': [[-1, False], [814, True], [1156, False]],
        '1921': [[-1, False], [506, True], [716, False], [969, True], [1259, False]]
    }

    difference_list = sorted([[item, page_index - item[0]] for item in
                              manual_begin_end_dict[year] if page_index - item[0] > 0],
                              key=itemgetter(1))

    in_column = difference_list[0][0][1]
    return in_column
