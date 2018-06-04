"""Split pages on columns."""

from ImageSaver import ImageSaver
from PIL import Image
import numpy as np
import pandas as pd
import statistics
import RunTimeData
import ImageColumnCropOperators

class ColumnCropper(object):

    def __init__(self, file_path, page_index, start_time, time_elapsed):

        self.file_path = file_path
        self.time_elapsed = RunTimeData.interim_print_statement(file_path, start_time, time_elapsed)
        self.img = ImageColumnCropOperators.open_image(self.file_path)
        self.crop_data = self.define_crop_point()
        self.luminance_img = self.crop_data[0]
        self.crop_point = self.crop_data[1]
        self.columns_list = self.perform_crop()

        for index, array in enumerate(self.columns_list):
            ImageSaver(self.file_path, array, index + 1)
            # Image.fromarray(array).show()

    def define_crop_point(self):
        """Crop images at center point into two column-arrays."""

        luminance_img = ImageColumnCropOperators.convert_image_luminance(self.img)
        rolling_mean = ImageColumnCropOperators.convert_rolling_mean(luminance_img, 0, 20, 0)
        edge_val = int(np.shape(luminance_img)[1] / 2.15)
        crop_array = ImageColumnCropOperators.crop_array(rolling_mean, edge_val)

        threshold = .95
        while True:
            white_points = list(crop_array.index[crop_array['values'] > threshold])
            if len(white_points) > 30:
                crop_point = int(statistics.median(white_points))
                break
            else:
                threshold -= .01

        return (luminance_img, crop_point)

    def perform_crop(self):
        """Crop columns and return list of arrays."""

        column_left = self.luminance_img[:, :self.crop_point]
        column_right = self.luminance_img[:, self.crop_point:]
        return (column_left, column_right)
