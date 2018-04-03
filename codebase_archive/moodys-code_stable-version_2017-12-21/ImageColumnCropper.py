"""ImageColumnCropper module; imported by ImageOperate aggregate class."""

from PIL import Image
import statistics
import numpy as np
import pandas as pd

class ImageColumnCropper(object):

    """
    Column cropping function; dynamically splits image on vertical columns.

    Attributes:
        final_cropped_array_list: Incoming image array of the full image.
        page_number_array: Incoming image array of the page number section crop.
        cutpoints: List of single-pixel integer values used to cut full image (e.g. [984, 1693]).
        output_images: Tuple of image arrays sent to ImageSaver function.
    """

    def __init__(self, rotated_image, array_input, iteration):

        self.iteration = iteration

        if self.iteration == 'vertical':
            self.final_cropped_array_list = array_input.output_images

        elif self.iteration == 'horizontal':
            self.final_cropped_array_list = [(np.rot90(array_input.final_cropped_array, k=3))]

        self.page_number_array = array_input.page_number_array
        self.threshold = rotated_image.threshold
        self.output_images = self.column_crop_operate()

    def column_cutter(self, image_array, cutpoints, iteration_list):
        """Crops full image array on defined crop points."""

        # Cut array on crop points; add cropped array segments to 'iteration_list'.
        working_image = image_array
        if len(cutpoints) > 0:
            for cut in cutpoints:

                column_right = working_image[:, cut:]
                column_left = working_image[:, 0:cut]

                if self.iteration == 'vertical':
                    iteration_list.append(column_right)

                elif self.iteration == 'horizontal':
                    iteration_list.append(np.rot90(column_right, k=1))

                if len(cutpoints) > 1:
                    working_image = column_left
                    continue

            if self.iteration == 'vertical':
                iteration_list.append(column_left)

            elif self.iteration == 'horizontal':
                iteration_list.append(np.rot90(column_left, k=1))

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def build_interval_dict(axis_rollmean, count_intervals):
        """Build intervals in which to search for columns."""

        # Take rolling mean of final cropped image array on horizontal axis (20 pixel intervals)
        # Take image width; define 5 horizontal pixel intervals.

        image_dimension = int(len(axis_rollmean))
        intervals = np.linspace(axis_rollmean.first_valid_index(), image_dimension, count_intervals)

        interval_dict = {}

        for i, bound in enumerate(intervals[:-1]):
            interval_dict.update({int(bound):int(intervals[i+1])})

        return interval_dict

    @staticmethod
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

    def clean_cutpoints_vertical(self, cutpoints_dict, distance_min, distance_max):
        """Cull cutpoints list to only include actual column gutters."""

        if len(cutpoints_dict) > 0:
            whiteness_cutoff = .99
            column_found = 0
            column_clear_iteration = 0

            dictionary_max = max([point for point, cut_pixel in cutpoints_dict.items() if point < 1])
            while column_found == 0:
                if whiteness_cutoff in [point for point, cut_pixel in cutpoints_dict.items()]:
                    for low_point in [low_point for low_point, cut_pixel in cutpoints_dict.items()
                                      if low_point < whiteness_cutoff]:

                        min_dif = min([abs(cut_pixel - cutpoints_dict[low_point])
                                       for high_point, cut_pixel in cutpoints_dict.items()
                                       if (high_point >= whiteness_cutoff
                                           and high_point < 1
                                           or high_point == 1 + dictionary_max)])

                        for high_point in [high_point for high_point, cut_pixel
                                           in cutpoints_dict.items()
                                           if (high_point >= whiteness_cutoff
                                               and high_point < 1
                                               or high_point == 1 + dictionary_max)]:

                            if (abs(cutpoints_dict[high_point] - cutpoints_dict[low_point]) == min_dif
                                and abs(cutpoints_dict[high_point] - cutpoints_dict[low_point]) < distance_min
                                or abs(cutpoints_dict[high_point] - cutpoints_dict[low_point]) > distance_max):

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

        return cutpoints_dict

    def clean_cutpoints_horizontal(self, cutpoints):

        for index, item in enumerate(self.final_cropped_array_list[0].T):
            if index in cutpoints:
                under_list = [value for value in item if value < 5]
                if len(under_list) > 50:
                    cutpoints.remove(index)

        return cutpoints

    @staticmethod
    def define_cutpoints(cutpoints_dict):
        cutpoints = []
        for count, val in cutpoints_dict.items():
            cutpoints.append(val)

        cutpoints.sort()
        cutpoints = sorted(cutpoints, reverse=True)

        # Return list 'cutpoints' to be used in above-defined Column Cutter function.
        return cutpoints

    def column_crop_operate(self):
        """Trigger class methods and produce final cutpoints list."""

        # Set base images into out_images.
        output_images = []
        iteration_list = []
        if self.iteration == 'vertical':
            output_images.extend(self.final_cropped_array_list)
            loop_list = [self.final_cropped_array_list[1]]

        elif self.iteration == 'horizontal':
            output_images.extend((self.page_number_array, np.rot90(self.final_cropped_array_list[0], k=1)))
            loop_list = self.final_cropped_array_list

        # Loop through loop_list and run operations.
        for image_array in loop_list:

            print(image_array)

            if self.iteration == 'vertical':
                rolling_mean = ImageColumnCropper.convert_rolling_mean(image_array, 0, 20, 400)
                interval_dict = ImageColumnCropper.build_interval_dict(rolling_mean, 5)
                cutpoints_dict_initial = ImageColumnCropper.find_cutpoints(self.threshold, interval_dict, rolling_mean, 0, 1)[1]
                cutpoints_dict_final = self.clean_cutpoints_vertical(cutpoints_dict_initial, 900, 1000)
                cutpoints = ImageColumnCropper.define_cutpoints(cutpoints_dict_final)

                self.column_cutter(image_array, cutpoints, iteration_list)
                output_images.append(iteration_list)

            elif self.iteration == 'horizontal':
                rolling_mean = ImageColumnCropper.convert_rolling_mean(image_array, 0, 20, 50)
                interval_dict = ImageColumnCropper.build_interval_dict(rolling_mean, 10)
                cutpoints_dict_final = ImageColumnCropper.find_cutpoints(self.threshold, interval_dict, rolling_mean, 30, 20)[1]
                cutpoints_initial = ImageColumnCropper.define_cutpoints(cutpoints_dict_final)
                cutpoints = self.clean_cutpoints_horizontal(cutpoints_initial)

        return output_images
