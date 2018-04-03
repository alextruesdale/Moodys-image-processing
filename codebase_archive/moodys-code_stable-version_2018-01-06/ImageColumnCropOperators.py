"""ImageColumnCropOperators module; imported by ImageOperate aggregate class."""

from PIL import Image
import statistics
import numpy as np
import pandas as pd

def column_cutter(image_array, cutpoints, iteration, iteration_list):
    """Crops full image array on defined crop points."""

    # Cut array on crop points; add cropped array segments to 'iteration_list'.
    working_image = image_array
    if len(cutpoints) > 0:
        for cut in cutpoints:

            column_right = working_image[:, cut:]
            column_left = working_image[:, 0:cut]

            if iteration == 'vertical':
                iteration_list.append(column_right)

            elif iteration == 'horizontal':
                iteration_list.append(np.rot90(column_right, k=1))

            if len(cutpoints) > 1:
                working_image = column_left
                continue

        if iteration == 'vertical':
            iteration_list.append(column_left)

        elif iteration == 'horizontal':
            iteration_list.append(np.rot90(column_left, k=1))

def convert_rolling_mean(array, axis, interval, offset):
    """Take rolling mean of image array."""

    if offset == 0:
        axis_rollmean = ((pd.DataFrame(list((array.mean(axis=axis)) / 255)))
                         .rolling(interval).mean())
    else:
        axis_rollmean = ((pd.DataFrame(list((array.mean(axis=axis)) / 255)))
                         .rolling(interval).mean()).iloc[offset : -(offset)]

    axis_rollmean.columns = ['values']
    return axis_rollmean

def convert_rolling_sdev(array, axis, interval, offset):
    """Take rolling sdev of image array."""

    if offset == 0:
        axis_rollsdev = ((pd.DataFrame(list((array.std(axis=axis)) / 255)))
                         .rolling(interval).std())
    else:
        axis_rollsdev = ((pd.DataFrame(list((array.std(axis=axis)) / 255)))
                         .rolling(interval).std()).iloc[offset : -(offset)]

    axis_rollsdev.columns = ['values']
    return axis_rollsdev

def build_interval_dict(axis_rollmean, count_intervals):
    """Build intervals in which to search for columns."""

    # Take rolling mean of final cropped image array on horizontal axis (20 pixel intervals)
    # Take image width; define 5 horizontal pixel intervals.

    image_dimension = len(axis_rollmean)
    intervals = np.linspace(axis_rollmean.first_valid_index(), image_dimension, count_intervals)

    interval_dict = {}

    for i, bound in enumerate(intervals[:-1]):
        interval_dict.update({int(bound):int(intervals[i+1])})

    return interval_dict

def find_cutpoints(whiteness_threshold, interval_dict, axis_rollmean, gutter_threshold_1, gutter_threshold_2):
    """Iterate through each interval open-close pair to find possible cutpoints"""

    cutpoints_dict = {}
    white_check_list = []

    for open_bound, close_bound in interval_dict.items():

        interval_range = axis_rollmean.iloc[open_bound : close_bound]

        run_loop = 0
        whiteness_score = .99
        while run_loop == 0:

            if whiteness_score <= whiteness_threshold - .02:
                break

            white_list = [i for i, r in interval_range.loc[interval_range['values']
                                                           > whiteness_score].iterrows()]

            if len(white_list) > gutter_threshold_1:

                white_check_list = []
                list_iterate = 0
                loop_offset = 0
                while list_iterate < len(white_list) - 1:
                    sub_check_list = []
                    for i, val in enumerate(white_list[:-1]):
                        if list_iterate < len(white_list) - 1:
                            if white_list[i + loop_offset] + 1 == white_list[i + loop_offset + 1]:
                                sub_check_list.append(white_list[i + loop_offset])
                                list_iterate += 1
                            else:
                                loop_offset = list_iterate + 1
                                list_iterate += 1
                                break

                    if len(sub_check_list) + 1 > gutter_threshold_2:
                        white_check_list.append(sub_check_list)
                        peak_id = int(statistics.median(sub_check_list)) - 5

                        if whiteness_score in cutpoints_dict.keys():
                            cutpoints_dict.update({round(whiteness_score + 1, 2) : peak_id})
                        else:
                            cutpoints_dict.update({round(whiteness_score, 2) : peak_id})

                run_loop = 1
            else:
                whiteness_score = round(whiteness_score - .01, 2)

    return (white_check_list, cutpoints_dict)

def define_cutpoints(cutpoints_dict):
    cutpoints = []
    for count, val in cutpoints_dict.items():
        cutpoints.append(val)

    cutpoints.sort()
    cutpoints = sorted(cutpoints, reverse=True)

    # Return list 'cutpoints' to be used in above-defined Column Cutter function.
    return cutpoints
