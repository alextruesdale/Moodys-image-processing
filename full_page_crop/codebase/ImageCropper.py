"""ImageCropper module; imported by ImageOperate aggregate class."""

import statistics
import ImageColumnCropOperators
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

pd.options.mode.chained_assignment = None

class ImageCropper(object):

    """
    Cropping function; removes black image borders and outputs cropped image without Moody's header.

    Attributes:
        final_rotate: Incoming straightened image object from the ImageRotater class.
        cropped_array: Cropped body portion of image as an array not including Moody's header.
        page_number_array: Cropped header portion of image as an array.
    """

    def __init__(self, rotated_image):

        self.final_rotate = rotated_image.final_rotate
        self.luminance_img = ImageColumnCropOperators.convert_image_luminance(self.final_rotate)
        self.cropped_array = self.rotate_crop_refine()
        self.final_cropped_array = self.trim_sides()

    def rotate_crop_refine(self):
        """Loop to identify crop points; examines image vertically, rotates 90°, repeats."""

        crop_pts = []
        for index in range(0, 2):

            # Rotate 90° for second treatment.
            if index == 1:
                self.luminance_img = np.rot90(self.luminance_img, k = 3)

            rolling_mean = ImageColumnCropOperators.convert_rolling_mean(self.luminance_img, 1, 20, 0)

            # Take the median dimension value of range of values with 'whiteness' greater than .65.
            white_score = .65
            split_val = 300
            split_list = ImageColumnCropOperators.split_array(rolling_mean, split_val)
            crop_pts_iteration = 0
            while crop_pts_iteration < 2:
                for split_range in split_list:
                    white_points = list(split_range.index[split_range['values'] > white_score])

                    if len(white_points) > 0:
                        if len(white_points) < 350:
                            if max(white_points) < (int(len(rolling_mean)) / 2):
                                white_range = int(min(white_points))
                            elif max(white_points) > (int(len(rolling_mean)) / 2):
                                white_range = int(max(white_points))
                        else:
                            white_range = int(statistics.median(white_points))

                        crop_pts.append(white_range)
                        crop_pts_iteration += 1
                        white_score = .70
                        split_val = 300
                        if crop_pts_iteration == 2:
                            break
                    else:
                        if split_range['values'].mean() < .5 and split_val < 700:
                            split_val += 100
                        else:
                            white_score -= .02

                        split_list = ImageColumnCropOperators.split_array(rolling_mean, split_val)
                        if crop_pts_iteration in [0, 2]:
                            break
                        elif crop_pts_iteration == 1:
                            split_list = split_list[::-1]
                            break

        # Rotate image back to upright; crop image on 'white_range' values.
        edge_trimmed_array = np.rot90(self.luminance_img, k = 1)
        cropped_array = edge_trimmed_array[crop_pts[0] : crop_pts[1],
                                           crop_pts[2] : crop_pts[3]]

        return cropped_array

    def trim_sides(self):
        """Trim extra white space from edges of page text; standardise images."""

        def build_array(array):
            """
            Construct dataframe noting decreasing brightness.
            This indicates approach of the edge of the page text.
            """

            rolling_mean_vertical_array = ImageColumnCropOperators.convert_rolling_mean(array, 0, 10, 0)
            split_value = int(len(rolling_mean_vertical_array) / 2)
            split_list = ImageColumnCropOperators.split_array(rolling_mean_vertical_array, split_value)

            iteration = 1
            array_var_list = []
            for array in split_list:

                # plt.plot(array)
                # plt.show()

                if iteration == 2:
                    array = array.iloc[::-1]

                array_shift = pd.DataFrame(array['values'].shift(-1))
                array_shift.columns = ['values']
                array['values2'] = array_shift['values']
                array['distance'] = array['values2'] - array['values']
                array['distance_binary'] = [0 if value >= 0 else 1 for value in array['distance']]

                array_shift2 = pd.DataFrame(array['distance_binary'].shift(-1))
                array_shift2.columns = ['distance']
                array['distance_binary_shift'] = array_shift2['distance']
                array['index'] = array.index
                array = array[['index', 'distance', 'distance_binary', 'distance_binary_shift']]

                array['distance'].fillna(0, inplace=True)
                array['distance_binary'].fillna(0, inplace=True)
                array['distance_binary_shift'].fillna(0, inplace=True)
                array['distance_binary'] = array['distance_binary'].astype(int)
                array['distance_binary_shift'] = array['distance_binary_shift'].astype(int)
                array = array.values.tolist()

                array_var_list.append(array)
                iteration += 1

            return (rolling_mean_vertical_array, array_var_list)

        def descending_continuity(input_data, run_type):
            """
            Evaluate movement from black edge-of-page to edge-of-text.
            Crop page in at edges of text w/ ~45px (or less) of padding.
            """

            rolling_mean_vertical_array = input_data[0]
            array_var_list = input_data[1]

            iteration = 1
            crop_points_inner = []
            for array in array_var_list:

                continuity = 0
                if run_type == 'original':
                    for distance_list in array:
                        if distance_list[2] == 1 and distance_list[3] == 1:
                            continuity += -(distance_list[1])
                            if continuity >= .013:
                                break
                        else:
                            continuity = 0

                # if run_type == 'second_pass':
                #     for distance_list in array:
                #         if distance_list[2] == 1 and distance_list[3] == 1:
                #             continuity += -(distance_list[1])
                #             if continuity >= .04:
                #                 break
                #         else:
                #             continuity = 0

                if iteration == 1:
                    if int(distance_list[0]) <= 45:
                        crop_points_inner.append(0)
                    else:
                        crop_points_inner.append(int(distance_list[0]) - 45)
                elif iteration == 2:
                    if len(rolling_mean_vertical_array) - int(distance_list[0]) <= 45:
                        crop_points_inner.append(len(rolling_mean_vertical_array))
                    else:
                        crop_points_inner.append(int(distance_list[0]) + 45)

                iteration += 1
            return crop_points_inner

        crop_points = []
        array_list = [self.cropped_array, np.rot90(self.cropped_array, k = 1)]
        for array in array_list:
            array_data = build_array(array)
            array_crop_pts = descending_continuity(array_data, 'original')

            for point in array_crop_pts:
                crop_points.append(point)

        trimmed_image = self.cropped_array[crop_points[2] : crop_points[3],
                                           crop_points[0] : crop_points[1]]

        # Image.fromarray(trimmed_image).show()

        # # Account for incomplete trimming on darker images.
        # array_data = build_array(trimmed_image)
        # array_crop_pts = descending_continuity(array_data, 'second_pass')
        #
        # if array_crop_pts[0] > 15:
        #     if array_crop_pts[0] > 100:
        #         array_crop_pts[0] = 100
        #     crop_points[0] = crop_points[0] + array_crop_pts[0]
        # elif (abs(array_crop_pts[1] - crop_points[1]) > 15 and
        #       abs(array_crop_pts[1] - crop_points[1]) < 100):
        #
        #     difference = abs(array_crop_pts[1] - crop_points[1])
        #     if difference > 20:
        #         difference = 20
        #     crop_points[1] = crop_points[1] - difference
        #
        # trimmed_image_out = self.cropped_array[crop_points[2] : crop_points[3],
        #                                        crop_points[0] : crop_points[1]]

        return trimmed_image
