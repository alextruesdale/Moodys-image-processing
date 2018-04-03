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

    def clean_cutpoints_vertical(self, image_array, cutpoints_final, offset):
        """Cull cutpoints list to only include actual column gutters."""

        image_width = image_array.shape[1]
        center_gutter = int(round(image_width/2, 0))
        one_third_gutter = int(round(1*(image_width/3), 0))
        two_third_gutter = int(round(2*(image_width/3), 0))

        print('IN:', cutpoints_final)
        print(one_third_gutter, two_third_gutter)

        if len(cutpoints_final) > 0 and len(cutpoints_final) <= 3:

            if len(cutpoints_final) <= 2 and any(x in list(range((center_gutter - offset), (center_gutter + offset), 1)) for x in cutpoints_final):

                diff_list = []
                for cutpoint in cutpoints_final:
                    diff_list.append(abs(center_gutter - cutpoint))

                min_diff_list = min(diff_list)
                for i, item in enumerate(diff_list):
                    if item == min_diff_list:
                        cutpoint_half = cutpoints_final[i]

                remove_list = [value for value in cutpoints_final if value != cutpoint_half]

            elif (any(x in list(range((one_third_gutter - offset), (one_third_gutter + offset), 1)) for x in cutpoints_final) and
                  any(x in list(range((two_third_gutter - offset), (two_third_gutter + offset), 1)) for x in cutpoints_final)):

                 i = 1
                 cutpoints_thirds = []
                 for value in [one_third_gutter, two_third_gutter]:
                     diff_list = []
                     for cutpoint in cutpoints_final:
                         diff_list.append(abs(value - cutpoint))

                     min_diff_list = min(diff_list)
                     for iteration, item in enumerate(diff_list):
                         if item == min_diff_list:
                             cutpoints_thirds.append(cutpoints_final[iteration])
                     i += 1

                 remove_list = [value for value in cutpoints_final if value not in cutpoints_thirds]

            else:
                remove_list = cutpoints_final

        else:
            remove_list = cutpoints_final

        cutpoints_final = [value for value in cutpoints_final if value not in remove_list]
        print('OUT:', cutpoints_final)
        return cutpoints_final

    def vertical_gutter_test(self):

        if len(self.cutpoints) == 0:
            horizontal_run_test = True
        else:
            horizontal_run_test = False

        print(horizontal_run_test)
        return horizontal_run_test

    def column_crop_operate(self, test_value):
        """Trigger class methods and produce final cutpoints list."""

        # Set base images into out_images.
        output_images = []
        iteration_list = []
        output_images.extend(self.final_cropped_array_list)

        if test_value == True:
            print('vertical_test')
            loop_list = [self.final_cropped_array_list]
        else:
            print('vertical_run')
            if len(self.final_cropped_array_list[2]) > 0:
                loop_list = self.final_cropped_array_list[2]
            else:
                loop_list = [self.final_cropped_array_list[1]]

        # Loop through loop_list and run operations.
        horizontal_ocr_list = []
        for image_array in loop_list:
            rolling_mean = ImageColumnCropOperators.convert_rolling_mean(image_array,
                                                                         0, 20, 400)

            cutpoints_initial = ImageColumnCropOperators.find_cutpoints(
                                image_array, (self.threshold - .01), rolling_mean, 20)[1]

            cutpoints_final = ImageColumnCropOperators.list_clean(image_array, cutpoints_initial, 100, 5, 20)

            cutpoints = self.clean_cutpoints_vertical(image_array, cutpoints_final, 60)

            if len(cutpoints) == 0:
                horizontal_ocr_list.append(1)
            else:
                horizontal_ocr_list.append(0)

            if test_value == False:
                ImageColumnCropOperators.column_cutter(image_array, cutpoints, self.iteration, iteration_list)
                output_images.append(iteration_list)

        return (cutpoints, output_images, horizontal_ocr_list)
