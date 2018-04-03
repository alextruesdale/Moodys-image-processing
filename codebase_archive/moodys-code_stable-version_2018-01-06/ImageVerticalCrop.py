"""ImageColumnCropper module; imported by ImageOperate aggregate class."""

from PIL import Image
import ImageColumnCropOperators
import statistics
import numpy as np
import pandas as pd

class ImageVerticalCrop(object):

    def __init__(self, rotated_image, array_input, test_value):

        self.iteration = 'vertical'
        if test_value == True:
            self.final_cropped_array_list = array_input.final_cropped_array
        else:
            self.final_cropped_array_list = array_input.output_images

        self.page_number_array = array_input.page_number_array
        self.threshold = rotated_image.threshold
        self.output_data = self.column_crop_operate(test_value)
        self.cutpoints = self.output_data[0]
        self.output_images = self.output_data[1]
        self.horizontal_ocr_list = self.output_data[2]

        if test_value == True:
            self.horizontal_run_test = self.vertical_gutter_test()

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

    def vertical_gutter_test(self):

        trimmed_matrix = self.final_cropped_array_list[100:-100, :]

        remove_list = []
        for cutpoint in self.cutpoints:
            check_list = list(range((cutpoint - 4), (cutpoint + 4), 1))

            interference_count = 0
            for index, item in enumerate(trimmed_matrix.T):
                if index in check_list:
                    under_list = [value for value in item if value < 5]
                    if len(under_list) > 20:
                        interference_count += 1

            if interference_count > 3:
                remove_list.append(cutpoint)

        for item in remove_list:
            self.cutpoints.remove(item)

        if len(self.cutpoints) == 0:
            horizontal_run_test = True
        else:
            horizontal_run_test = False

        return horizontal_run_test

    def column_crop_operate(self, test_value):
        """Trigger class methods and produce final cutpoints list."""

        # Set base images into out_images.
        output_images = []
        iteration_list = []
        output_images.extend(self.final_cropped_array_list)

        if test_value == True:
            loop_list = [self.final_cropped_array_list]
        else:
            if len(self.final_cropped_array_list[2]) > 0:
                loop_list = self.final_cropped_array_list[2]
            else:
                loop_list = [self.final_cropped_array_list[1]]

        # Loop through loop_list and run operations.
        horizontal_ocr_list = []
        for image_array in loop_list:

            rolling_mean = ImageColumnCropOperators.convert_rolling_mean(image_array, 0, 20, 400)
            interval_dict = ImageColumnCropOperators.build_interval_dict(rolling_mean, 5)
            cutpoints_dict_initial = ImageColumnCropOperators.find_cutpoints(self.threshold, interval_dict, rolling_mean, 0, 1)[1]
            cutpoints_dict_final = self.clean_cutpoints_vertical(cutpoints_dict_initial, 900, 1000)
            cutpoints = ImageColumnCropOperators.define_cutpoints(cutpoints_dict_final)

            if len(cutpoints) == 0:
                horizontal_ocr_list.append(1)
            else:
                horizontal_ocr_list.append(0)

            if test_value == False:
                ImageColumnCropOperators.column_cutter(image_array, cutpoints, self.iteration, iteration_list)
                output_images.append(iteration_list)

        return (cutpoints, output_images, horizontal_ocr_list)
