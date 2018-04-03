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

def list_clean(array, check_list, array_offset, column_offset, under_list_threshold):
    """"""

    trimmed_array = array[array_offset:-array_offset, :]

    remove_list = []
    for list_item in check_list:
        check_list_range = list(range((list_item - column_offset), (list_item + column_offset), 1))

        interference_count = 0
        for index, item in enumerate(trimmed_array.T):
            if index in check_list_range:
                under_list = [value for value in item if value < 5]
                if len(under_list) > under_list_threshold:
                    interference_count += 1

        if interference_count > 5:
            remove_list.append(list_item)

    check_list_out = [value for value in check_list if value not in remove_list]
    check_list_out.sort()
    check_list_out = sorted(check_list_out, reverse=True)

    return check_list_out

def find_cutpoints(array, whiteness_threshold, axis_rollmean, gutter_threshold):
    """Iterate through each interval open-close pair to find possible cutpoints"""

    whiteness_score = whiteness_threshold
    white_list = [i for i, r in axis_rollmean.loc[axis_rollmean['values']
                                                  > whiteness_score].iterrows()]

    cutpoints = []
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

        if len(sub_check_list) + 1 > gutter_threshold:
            white_check_list.append(sub_check_list)
            peak_id = int(statistics.median(sub_check_list))
            cutpoints.append(peak_id)
    print(cutpoints)
    return (white_check_list, cutpoints)
