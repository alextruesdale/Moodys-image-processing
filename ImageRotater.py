"""ImageRotater module; imported by ImageOperate aggregate class."""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class ImageRotater(object):

    """
    Rotater function; straightens image to expected vertical format.

    Attributes:
        file: Incoming instance file path (e.g './tif/test/one/Banks19280011-0006.tif').
        img: Editable image object; opened from 'file' variable.
        max_point: Final rotation point in degrees (e.g. 361.4) to be applied to instance image.
        final_rotate: Straighted image to be sent forward for further processing.
    """

    def __init__(self, file):

        self.file = file
        self.img = self.open_image()
        self.max_point = self.rotate_on_curve()
        self.final_rotate = self.img_rotate_operate()

    def open_image(self):
        """Open images from 'files' list."""

        img = Image.open(self.file)
        return img

    def rotate_check(self, x_value, anchor_points):
        """Rotate image and check vertical whiteness. Produce anchor points for polynomial curve."""

        # Rotate image by loop-value 'x_value'
        img_rotated = self.img.rotate(x_value, expand=1)

        # Convert rotated image to luminance array
        img_luminance = np.asarray((img_rotated).convert('L'))

        # Take internal slice of image to test for vertical whitespace.
        internal = int(round((len(img_luminance) / 7), 0))
        border_cropped = img_luminance[internal : -internal, internal : -internal]

        # Convert luminance array to list; average pixel density per column (vertical axis).
        axis_y = list((border_cropped.mean(axis=0)) / 255)

        def vertical_cutoff(vertical_value):
            """Find 'whiteness scores' greater than .95"""
            return vertical_value > .97

        y_value = sum(1 for vertical_value in axis_y if vertical_cutoff(vertical_value))

        # Add [x, y] coordinates do anchor-point list 'anchor_points'.
        anchor_points.append([x_value, y_value])

    def rotate_on_curve(self):
        """Create polynomial curve and derive optimal rotation degree."""

        # Write list of six points between bounding points 359.4, 361.5; degrees for image rotation
        points = list(np.linspace(359.4, 361.5, 7))
        anchor_points = []

        # For each of these points, perform the above-defined Rotate and Check function.
        for point in points:

            self.rotate_check(point, anchor_points)

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
        plt.plot(x_values, y_values, 'o', x_new, y_new)
        plt.xlim([x_values[0]-1, x_values[-1] + 1])
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
        final_rotate = self.img.rotate(self.max_point, expand=1)

        # Return final rotated image to be sent on for further processing.
        return final_rotate
