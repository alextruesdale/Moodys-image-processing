"""ImageColumnCropper module; imported by ImageOperate aggregate class."""

from PIL import Image
import ImageColumnCropOperators
import statistics
import numpy as np
import pandas as pd

class ImageHorizontalCrop(object):

    def __init__(self, rotated_image, array_input, vertical_gutter_test):

        self.operate = vertical_gutter_test.horizontal_run_test

        self.iteration = 'horizontal'
        self.final_cropped_array_list = [(np.rot90(array_input.final_cropped_array, k=3))]
        self.page_number_array = array_input.page_number_array
        self.threshold = rotated_image.threshold
        self.output_images = self.column_crop_operate()

    def clean_cutpoints_horizontal(self, cutpoints):

        for index, item in enumerate(self.final_cropped_array_list[0].T):
            if index in cutpoints:
                under_list = [value for value in item if value < 5]
                if len(under_list) > 50:
                    cutpoints.remove(index)

        return cutpoints

    def column_crop_operate(self):
        """Trigger class methods and produce final cutpoints list."""

        # Set base images into out_images.
        output_images = []
        iteration_list = []
        output_images.extend((self.page_number_array, np.rot90(self.final_cropped_array_list[0], k=1)))

        # Loop through loop_list and run operations.
        if self.operate == True:
            for image_array in self.final_cropped_array_list:

                rolling_mean = ImageColumnCropOperators.convert_rolling_mean(image_array, 0, 20, 50)
                interval_dict = ImageColumnCropOperators.build_interval_dict(rolling_mean, 10)
                cutpoints_dict_final = ImageColumnCropOperators.find_cutpoints(self.threshold, interval_dict, rolling_mean, 30, 20)[1]
                cutpoints_initial = ImageColumnCropOperators.define_cutpoints(cutpoints_dict_final)
                cutpoints = self.clean_cutpoints_horizontal(cutpoints_initial)

                ImageColumnCropOperators.column_cutter(image_array, cutpoints, self.iteration, iteration_list)
                output_images.append(iteration_list)
        else:
            output_images.append(iteration_list)
            
        return output_images
