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
        self.cutpoints = self.find_columns()
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

    def find_columns(self):
        """Find columns and define crop points for cutting function."""

        # Take rolling mean of final cropped image array on horizontal axis (20 pixel intervals)
        # Take image width; define 5 horizontal pixel intervals.
        axis_x_rollmean = ((pd.DataFrame(list((self.final_cropped_array.mean(axis=0)) / 255)))
                           .rolling(20).mean()).iloc[400 : -400]

        image_width = len(axis_x_rollmean)
        intervals = np.linspace(axis_x_rollmean.first_valid_index(), image_width, 5)

        window_dict = {}
        cutpoints = []

        for i, bound in enumerate(intervals[:-1]):
            window_dict.update({int(bound):int(intervals[i+1])})

        # Check each interval for spikes in whiteness (>.98 'whiteness score')
        # Take median of these ranges & add to 'cutpoints' list.
        for open_bound, close_bound in window_dict.items():

            interval_range = axis_x_rollmean.iloc[open_bound : close_bound]
            interval_range.columns = ['values']

            column_iteration = 0
            peak_id = 0
            whitness_score = .99
            while peak_id == 0:

                white_list = [i for i, r in interval_range.loc[interval_range['values']
                                                               > whitness_score].iterrows()]
                white_check_list = []
                for i, val in enumerate(white_list[:-1]):
                    if (val + 1) == white_list[i+1]:
                        white_check_list.append(val)

                if 38 < len(white_check_list) < 55:
                    peak_id = int(statistics.median(white_check_list))
                    cutpoints.append(peak_id)
                    break
                else:
                    whitness_score -= .01
                    column_iteration += 1

                if column_iteration > 4:
                    break

        # Remove one of pair ot cutpoints within 100 pixels of each other
        # (likely due to intervals landing in middle of column).
        cutpoints.sort()
        remove = [abs(x) for i, x in enumerate(np.diff(cutpoints)) if x < 300]

        for i, point in enumerate(cutpoints[:-1]):
            if abs(cutpoints[i + 1] - point) in remove:
                del cutpoints[i]

        cutpoints = sorted(cutpoints, reverse=True)

        # Return list 'cutpoints' to be used in above-defined Column Cutter function.
        return cutpoints
