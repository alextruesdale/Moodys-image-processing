"""ImageOperator module called by Main function."""

from ImageRotater import ImageRotater
from ImageCropper import ImageCropper
from ImageSaver import ImageSaver
from operator import itemgetter

import sys
sys.path.append('../../runtime_data/')
import RunTimeData

class ImageOperator(object):

    """
    Aggregate operator function; performs rotation, cropping, column cropping, and saving functions.

    Attributes:
        file: Path of file in original directory.
        rotated_image: Resulting instance of ImageRotater class.
        cropped_image_full: Resulting instance of ImageCropper class.
        save_images: Resulting instance of ImageSaver class.
    """

    def __init__(self, file_path, year, page_index, start_time, time_elapsed):

        self.file = file_path
        self.year = year
        self.page_index = page_index
        self.time_elapsed = RunTimeData.time_elapsed_placeholder(start_time)
        self.run_key = self.run_filter()

        if self.run_key:
            self.time_elapsed = RunTimeData.interim_print_statement(file_path, start_time, time_elapsed)
            self.rotated_image = ImageRotater(self.file, self.page_index, self.year)
            self.cropped_image_full = ImageCropper(self.rotated_image)
            ImageSaver(self.file, self.cropped_image_full)

    def run_filter(self):
        """Determine whether or not to operate on incoming class file."""

        manual_begin_end_dict = {
            '1920': [[-1, False], [134, True], [1513, False]],
            '1921': [[-1, False], [158, True], [1750, False]],
            '1922': [[-1, False], [193, True], [2077, False]],
            '1923': [[-1, False], [159, True], [2414, False]],
            '1924': [[-1, False], [310, True], [2878, False]],
            '1925': [[-1, False], [225, True], [2405, False]],
            '1926': [[-1, False], [270, True], [2665, False]],
            '1927': [[-1, False], [306, True], [3057, False]],
            '1928': [[-1, False], [348, True], [3425, False]],
            '1929': [[-1, False], [391, True], [3485, False]]
        }

        difference_list = sorted([[item, self.page_index - item[0]] for item in
                                  manual_begin_end_dict[self.year] if self.page_index - item[0] > 0],
                                  key=itemgetter(1))

        run_key = difference_list[0][0][1]
        return run_key
