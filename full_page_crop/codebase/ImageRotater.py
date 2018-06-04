"""ImageRotater module; imported by ImageOperate aggregate class."""

from PIL import Image
import ImageColumnCropOperators
import ColumnWindowFinder
import matplotlib.pyplot as plt
import numpy as np

class ImageRotater(object):

    """
    Rotater function; straightens image to expected vertical format.

    Attributes:
        file: Incoming instance file path (e.g './tif/test/one/Banks19280011-0006.tif').
        img: Editable image object; opened from 'file' variable.
        img_rotated:
        max_point: Final rotation point in degrees (e.g. 361.4) to be applied to instance image.
        final_rotate: Straighted image to be sent forward for further processing.
    """

    def __init__(self, file_path, page_index, year):

        self.file_path = file_path
        self.page_index = page_index
        self.year = year
        print(self.page_index)

        self.img = ImageColumnCropOperators.open_image(self.file_path)
        self.img_edged = self.edge_white_crop()

        if ColumnWindowFinder.run_filter(self.page_index, self.year):
            self.img_rotated = self.img_edged
            self.white_count_threshold = 30
            self.inner_denominator = 3

        else:
            self.img_rotated = self.img_edged.rotate(90, expand = 1)
            self.white_count_threshold = 450
            self.inner_denominator = 7

        self.max_point = self.rotate_on_curve()
        self.final_rotate = self.img_rotate_operate()

    def edge_white_crop(self):
        """Check edges for white bleed (non-black space)."""

        crop_pts = []
        luminance_img = ImageColumnCropOperators.convert_image_luminance(self.img)
        rolling_mean = ImageColumnCropOperators.convert_rolling_mean(luminance_img, 0, 20, 0)

        white_score = .6
        split_val = 100
        split_list = ImageColumnCropOperators.split_array(rolling_mean, split_val)
        for split_range in split_list:
            white_points = list(split_range.index[split_range['values'] > white_score])

            if len(white_points) > 0:
                if max(white_points) < (int(len(rolling_mean)) / 2):
                    white_range = int(max(white_points))
                elif max(white_points) > (int(len(rolling_mean)) / 2):
                    white_range = int(min(white_points))

                crop_pts.append(white_range)

        offset = 30
        if len(crop_pts) == 1:
            if crop_pts[0] < (int(len(rolling_mean)) / 2):
                edge_trimmed_array = luminance_img[:, crop_pts[0] + offset:]
            elif crop_pts[0] > (int(len(rolling_mean)) / 2):
                edge_trimmed_array = luminance_img[:, :crop_pts[0] - offset]

        elif len(crop_pts) == 2:
            edge_trimmed_array = luminance_img[:, crop_pts[0] + offset : crop_pts[1] - offset]

        else:
            edge_trimmed_array = luminance_img[:, :]

        edge_trimmed_image = Image.fromarray(edge_trimmed_array)
        return edge_trimmed_image

    def rotate_check(self, x_value, anchor_points, sheet_whiteness_list, threshold, inner_denominator, axis, override):
        """Rotate image and check vertical whiteness. Produce anchor points for polynomial curve."""

        # Rotate image by loop-value 'x_value'
        img_rotated = self.img_rotated.rotate(x_value, expand = 1)

        # Convert rotated image to luminance array
        img_luminance = ImageColumnCropOperators.convert_image_luminance(img_rotated)

        # Take internal slice of image to test for vertical whitespace.
        internal = int(round((len(img_luminance) / inner_denominator), 0))

        def crop_subsection(override, internal, axis, inner_denominator, top_offset):
            """Crop subsection for rotate test."""

            if override == False:
                border_cropped = img_luminance[internal : -internal, internal : -internal]
                sheet_whiteness = sum(1 for value in border_cropped.mean(axis = axis) if value > 250)
                sheet_whiteness_list.append(sheet_whiteness)
            elif override == True:
                internal_modified = int(round((len(img_luminance) / inner_denominator), 0))

                if ColumnWindowFinder.run_filter(self.page_index, self.year):
                    border_cropped = img_luminance[300 : -internal_modified, internal : -internal]
                else:
                    border_cropped = img_luminance[300 : -internal, internal : -internal_modified]

            return border_cropped

        if ColumnWindowFinder.run_filter(self.page_index, self.year):
            border_cropped = crop_subsection(override, internal, 1, 1.8, 400)
        else:
            border_cropped = crop_subsection(override, internal, 0, 4, 300)

        # Convert luminance array to list; average pixel density per column (vertical axis).
        axis_y = list((border_cropped.mean(axis = axis)) / 255)

        def vertical_cutoff(vertical_value):
            """Find 'whiteness scores' greater than .97"""
            return vertical_value > threshold

        y_value = sum(1 for vertical_value in axis_y if vertical_cutoff(vertical_value))

        # Add [x, y] coordinates do anchor-point list 'anchor_points'.
        anchor_points.append([x_value, y_value])
        return sheet_whiteness_list

    def rotate_on_curve(self):
        """Create polynomial curve and derive optimal rotation degree."""

        # Write list of six points between bounding points 356.8, 363.2; degrees for image rotation
        points = list(np.linspace(356.8, 363.2, 7))

        # For each of these points, perform the above-defined Rotate and Check function.
        threshold = .97
        while True:
            anchor_points = []
            sheet_whiteness_list = []
            for point in points:
                self.rotate_check(point, anchor_points, sheet_whiteness_list, threshold,
                                  self.inner_denominator, 0, False)

            if sum(1 for value in sheet_whiteness_list if value > 1000) >= 3:
                anchor_points = []
                sheet_whiteness_list = []
                for point in points:
                    self.rotate_check(point, anchor_points, sheet_whiteness_list, threshold,
                                      self.inner_denominator, 0, True)

            found_whiteness = [anchor_point[1] for anchor_point in anchor_points]

            if any(value > self.white_count_threshold for value in found_whiteness):
                break
            else:
                threshold -= .01

        # Convert 'anchor_points' list to NumPy Array; define 'x' and 'y' values from array pairs.
        anchor_points = np.array(anchor_points)
        x_values = [anchor_points[0] for anchor_points in anchor_points]
        y_values = [anchor_points[1] for anchor_points in anchor_points]

        # Calculate polynomial using 'x' and 'y' coordinates.
        poly_fit = np.polyfit(x_values, y_values, 4)
        poly_dimension = np.poly1d(poly_fit)

        # Calculate new 'x' and 'y' values for points along polynomial curve.
        x_new = np.linspace(x_values[0], x_values[-1], 150)
        y_new = poly_dimension(x_new)

        # Create plot of polynomial curve (currently set to hidden).
        # plt.plot(x_values, y_values, 'o', x_new, y_new)
        # plt.xlim([x_values[0]-1, x_values[-1] + 1])
        # plt.show()

        # Create lists of 'x' and 'y' values for all points along curve.
        x_vals = x_new.tolist()
        y_vals = y_new.tolist()

        # Transfer points to dictionary format {key : value} for x_values with highest y_value.
        plt_dictionary = (dict(zip(x_vals, y_vals)))
        max_coord = max((zip(plt_dictionary.values(), plt_dictionary.keys())))
        max_point = (max_coord[1])

        # Return 'max_point' for final rotation.
        return max_point

    def img_rotate_operate(self):
        """Run final rotation of source image to optimised degree."""

        # Run a final image rotation using 'max_point' from Rotate on Curve function.
        rotated_rotate = self.img_rotated.rotate(self.max_point, expand = 1)

        if ColumnWindowFinder.run_filter(self.page_index, self.year):
            final_rotate = rotated_rotate
        else:
            final_rotate = rotated_rotate.rotate(270, expand = 1)

        # Return final rotated image to be sent on for further processing.
        return final_rotate
