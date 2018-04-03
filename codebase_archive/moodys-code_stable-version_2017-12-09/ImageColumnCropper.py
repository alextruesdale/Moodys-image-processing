"""ImageColumnCropper module; imported by ImageOperate aggregate class."""

import statistics
import numpy as np
import pandas as pd

class ImageColumnCropper(object):

    """
    Column cropping function; dynamically splits image on vertical columns.

    Attributes:
        final_cropped_array: Incoming image array of the full image.
        page_number_array: Incoming image array of the page number section crop.
        cutpoints: List of single-pixel integer values used to cut full image (e.g. [984, 1693]).
        number_columns: String variable indicating image type ('three-column', 'two-column', etc.).
        output_images: Tuple of image arrays sent to ImageSaver function.
    """

    def __init__(self, cropped_image_full):

        self.final_cropped_array = cropped_image_full.final_cropped_array
        self.page_number_array = cropped_image_full.page_number_array
        self.cutpoints = self.column_crop_operate()
        self.column_data = self.column_cutter()
        self.number_columns = self.column_data[0]
        self.output_images = self.column_data[1]

    def column_cutter(self):
        """Crops full image array on defined crop points."""

        # Add 'final_cropped_array', 'page_number_array' to 'output_images' list.
        output_images = []
        output_images.extend((self.final_cropped_array, self.page_number_array))

        # Define 'number_columns' based on result of Find_Columns function below.
        if len(self.cutpoints) == 2:
            number_columns = 'three-column/'
        elif len(self.cutpoints) == 1:
            number_columns = 'two-column/'
        elif len(self.cutpoints) == 0:
            number_columns = 'one-column/'

        # Cut array on crop points; add cropped array segments so 'output_images'.
        working_image = self.final_cropped_array
        if len(self.cutpoints) > 0:
            for cut in self.cutpoints:

                column_right = working_image[:, cut:]
                column_left = working_image[:, 0:cut]

                output_images.append(column_right)

                if len(self.cutpoints) > 1:

                    working_image = column_left
                    continue

            output_images.append(column_left)

        # Return number of columns variable and list of output image arrays for writing/saving.
        return (number_columns, output_images)

    def build_interval_dict(self):
        """Build intervals in which to search for columns; construct rolling mean array."""

        # Take rolling mean of final cropped image array on horizontal axis (20 pixel intervals)
        # Take image width; define 5 horizontal pixel intervals.
        axis_rollmean = ((pd.DataFrame(list((self.final_cropped_array.mean(axis=0)) / 255)))
                         .rolling(20).mean()).iloc[400 : -(400)]

        axis_rollmean.columns = ['values']

        image_dimension = len(axis_rollmean)
        intervals = np.linspace(axis_rollmean.first_valid_index(), image_dimension, 5)

        interval_dict = {}

        for i, bound in enumerate(intervals[:-1]):
            interval_dict.update({int(bound):int(intervals[i+1])})

        return (interval_dict, axis_rollmean)

    def find_cutpoints(self, interval_dict, axis_rollmean):
        """Iterate through each interval open-close pair to find possible cutpoints"""

        cutpoints_dict = {}

        for open_bound, close_bound in interval_dict.items():

            interval_range = axis_rollmean.iloc[open_bound : close_bound]

            column_iteration = 0
            peak_id = 0
            whiteness_score = .99
            while peak_id == 0:
                white_list = [i for i, r in interval_range.loc[interval_range['values']
                                                               > whiteness_score].iterrows()]
                white_check_list = []
                for i, val in enumerate(white_list[:-1]):
                    if (val + 1) == white_list[i+1]:
                        white_check_list.append(val)

                if len(white_check_list) > 0:
                    peak_id = int(statistics.median(white_check_list))
                    if whiteness_score in cutpoints_dict.keys():
                        cutpoints_dict.update({round(whiteness_score + 1, 2) : peak_id})
                    else:
                        cutpoints_dict.update({round(whiteness_score, 2) : peak_id})
                    break
                else:
                    whiteness_score = round(whiteness_score - .01, 2)
                    column_iteration += 1

                if column_iteration > 10:
                    break

        return cutpoints_dict

    def clean_cutpoints(self, cutpoints_dict):
        """Cull cutpoints list to only include actual column gutters."""

        if len(cutpoints_dict) > 0:
            whiteness_cutoff = .99
            column_found = 0
            column_clear_iteration = 0

            while column_found == 0:
                if whiteness_cutoff in [point for point, cut_pixel in cutpoints_dict.items()]:
                    for low_point in [low_point for low_point, cut_pixel in cutpoints_dict.items()
                                      if low_point < whiteness_cutoff]:

                        min_dif = min([abs(cut_pixel - cutpoints_dict[low_point])
                                       for high_point, cut_pixel in cutpoints_dict.items()
                                       if high_point >= whiteness_cutoff])

                        for high_point in [high_point for high_point, cut_pixel
                                           in cutpoints_dict.items()
                                           if high_point >= whiteness_cutoff]:

                            if (abs(cutpoints_dict[high_point] - cutpoints_dict[low_point]) == min_dif
                                and abs(cutpoints_dict[high_point] - cutpoints_dict[low_point]) < 900
                                or abs(cutpoints_dict[high_point] - cutpoints_dict[low_point]) > 1000):

                                del cutpoints_dict[low_point]
                                if round(low_point + 1, 2) in cutpoints_dict:
                                    del cutpoints_dict[round(low_point + 1, 2)]
                                break
                    column_found = 1
                else:
                    whiteness_cutoff = round(whiteness_cutoff - .01, 2)
                    column_clear_iteration += 1

                if column_clear_iteration > 20:
                    break

        print('cutpoints:', cutpoints_dict)
        cutpoints = []
        for count, val in cutpoints_dict.items():
            cutpoints.append(val)

        cutpoints.sort()
        cutpoints = sorted(cutpoints, reverse=True)

        # Return list 'cutpoints' to be used in above-defined Column Cutter function.
        return cutpoints

    def column_crop_operate(self):
        """Trigger class methods and produce final cutpoints list."""

        interval_data = self.build_interval_dict()
        cutpoints_dict = self.find_cutpoints(interval_data[0], interval_data[1])
        cutpoints = self.clean_cutpoints(cutpoints_dict)

        return cutpoints
