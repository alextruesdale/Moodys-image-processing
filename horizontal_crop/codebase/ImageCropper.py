"""ImageCropper module; imported by ImageOperate aggregate class."""

from PIL import Image
import ImageColumnCropOperators
import statistics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
        self.rotate_crop_data = self.rotate_crop()
        self.cropped_array = self.rotate_crop_data[0]
        self.page_number_array = self.rotate_crop_data[1]
        self.final_cropped_array = self.trim_sides()

    def rotate_crop(self):
        """Define crop points and perform cropping."""

        crop_pts = []

        # Convert rotated image to luminance array
        luminance_img = np.asarray((self.final_rotate).convert('L'))

        # Loop to identify crop points; examines image vertically, rotates 90°, repeats.
        for index in range(0, 2):

            # Rotate 90° for second treatment.
            if index == 1:
                luminance_img = np.rot90(luminance_img, k=3)

            # Take column average pixel density.
            axis_avgs = list((luminance_img.mean(axis=1)) / 255)

            # Convert array to pd DataFrame; take rolling mean of avgs (30px per iteration).
            axis_df = pd.DataFrame(axis_avgs, columns=['values'])
            rolling_mean = axis_df.rolling(30).mean()

            # Crop array to only show edges of image (300 pixels from left & right).
            split_val = 300
            split1 = rolling_mean.iloc[: split_val]
            split2 = rolling_mean.iloc[-(split_val) :]
            split_list = [split1, split2]

            # Take the median dimension value of range of values with 'whiteness' greater than .85.
            crop_pts_iteration = 0
            white_score = .85
            while crop_pts_iteration < 2:
                for split_range in split_list:
                    white_points = list(split_range.index[split_range['values'] > white_score])

                    if len(white_points) > 0:
                        if len(white_points) < 50:
                            if max(white_points) < (int(len(rolling_mean)) / 2):
                                white_range = int(min(white_points))
                            elif max(white_points) > (int(len(rolling_mean)) / 2):
                                white_range = int(max(white_points))
                        else:
                            white_range = int(statistics.median(white_points))

                        crop_pts.append(white_range)
                        crop_pts_iteration += 1
                        white_score = .85
                        split_val = 300
                        if crop_pts_iteration == 2:
                            break
                    else:
                        if split_range['values'].mean() < .5 and split_val < 600:
                            split_val += 100
                        else:
                            white_score -= .02

                        split1 = rolling_mean.iloc[: split_val]
                        split2 = rolling_mean.iloc[-(split_val) :]
                        split_list = [split1, split2]
                        if crop_pts_iteration in [0, 2]:
                            break
                        elif crop_pts_iteration == 1:
                            split_list = [split2, split1]
                            break

        # Rotate image back to upright; crop image on 'white_range' values.
        luminance_img = np.rot90(luminance_img, k=1)
        cropped_img = luminance_img[crop_pts[0] : crop_pts[1],
                                    crop_pts[2] + 1250 : crop_pts[3] -1250]
        cropped_df = pd.DataFrame(list((cropped_img.mean(axis=1)) / 255), columns=['values'])

        # Slice top 1000 pixels to identify page header.
        cut_value = 1000
        bar_value = .1
        header_crop = 0

        header_iteration = 0
        while header_crop == 0:
            header_slice = cropped_df[:cut_value]
            if len(list(header_slice.index[header_slice['values'] < bar_value])) > 0:
                header_crop = max(list(header_slice.index[header_slice['values'] < bar_value]))
                crop_pts[0] = crop_pts[0] + header_crop
                break
            else:
                bar_value += .02
                header_iteration += 1

            if header_iteration > 5:
                break

        # Look for eronious bottom-of-page elements to crop out as well.
        footer_crop = 0

        footer_iteration = 0
        while footer_crop == 0:
            footer_slice = cropped_df[-cut_value:]
            if len(list(footer_slice.index[footer_slice['values'] < bar_value])) > 0:
                footer_crop = min(list(footer_slice.index[footer_slice['values'] < bar_value]))
                crop_pts[1] = crop_pts[0] - header_crop + footer_crop
                break
            else:
                bar_value += .02
                footer_iteration += 1

            if footer_iteration > 5:
                break

        # Crop final image to remove extra elements removed.
        cropped_array = luminance_img[crop_pts[0] : crop_pts[1],
                                            crop_pts[2] : crop_pts[3]]

        page_number_array = luminance_img[0 : crop_pts[0],
                                          crop_pts[2] : crop_pts[3]]

        # Return final cropped image and page number array for further processing.
        return (cropped_array, page_number_array)

    def trim_sides(self):
        """"""

        def build_array(array):
            """"""

            rolling_mean_vertical_array = ImageColumnCropOperators.convert_rolling_mean(array, 0, 10, 0)

            split_value = int(len(rolling_mean_vertical_array) / 2)
            vertical_array_split1 = rolling_mean_vertical_array.iloc[:split_value]
            vertical_array_split2 = rolling_mean_vertical_array.iloc[-split_value:]

            split_list = [vertical_array_split1, vertical_array_split2]

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
            """"""

            rolling_mean_vertical_array = input_data[0]
            array_var_list = input_data[1]

            iteration = 1
            crop_points_inner = []
            for array in array_var_list:

                continuity = 0
                break_point = 0
                if run_type == 'original':
                    for i, distance_list in enumerate(array):
                        if distance_list[2] == 1 and distance_list[3] == 1:
                            continuity += -(distance_list[1])
                            if continuity >= .025:
                                break
                        else:
                            continuity = 0

                if run_type == 'second_pass':
                    for i, distance_list in enumerate(array):
                        if distance_list[2] == 1 and distance_list[3] == 1:
                            continuity += -(distance_list[1])
                            if continuity >= .07:
                                break
                        else:
                            continuity = 0

                if iteration == 1:
                    if int(distance_list[0]) < 35:
                        crop_points_inner.append(0)
                    else:
                        crop_points_inner.append(int(distance_list[0]) - 35)
                elif iteration == 2:
                    if len(rolling_mean_vertical_array) - int(distance_list[0]) < 35:
                        crop_points_inner.append(len(rolling_mean_vertical_array))
                    else:
                        crop_points_inner.append(int(distance_list[0]) + 35)

                iteration += 1
            return crop_points_inner

        crop_points = []

        array_list = [self.cropped_array, np.rot90(self.cropped_array, k=1)]
        for array in array_list:
            array_data = build_array(array)
            array_crop_pts = descending_continuity(array_data, 'original')

            for point in array_crop_pts:
                crop_points.append(point)

        print(crop_points)

        trimmed_image = self.cropped_array[crop_points[2] : crop_points[3], crop_points[0] : crop_points[1]]

        # Account for incomplete trimming on darker images.
        array_data = build_array(trimmed_image)
        array_crop_pts = descending_continuity(array_data, 'second_pass')

        if array_crop_pts[0] > 7:
            if array_crop_pts[0] > 100:
                array_crop_pts[0] = 100
            crop_points[0] = crop_points[0] + array_crop_pts[0]
        elif abs(array_crop_pts[1] - crop_points[1]) > 7 and abs(array_crop_pts[1] - crop_points[1]) < 100:
            difference = abs(array_crop_pts[1] - crop_points[1])
            if difference > 25:
                difference = 25
            crop_points[1] = crop_points[1] - difference

        print(crop_points)

        trimmed_image_out = self.cropped_array[crop_points[2] : crop_points[3], crop_points[0] : crop_points[1]]
        return trimmed_image_out
