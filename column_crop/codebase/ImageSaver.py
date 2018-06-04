"""ImageSaver module; imported by ImageOperate aggregate class."""

import os
import shutil
from PIL import Image

class ImageSaver(object):

    """
    The column cropping function to be applied to each image, dynamically splitting it
    on vertical columns.

    Attributes:
        file: Path of file in original directory.
        output_image: Incoming image array to be written as images, saved.
        save_folder: Path of save folder for instance image.
    """

    def __init__(self, file_input, image_input, index):

        self.file_input = file_input
        self.output_image = image_input
        self.index = index
        self.image_save()

    def image_save(self):
        """Write image arrays as images and save them into the correct save folder."""

        if os.path.exists(self.file_input):
            os.remove(self.file_input)

        save_path = self.file_input[:-4] + '_column_{}'.format(str(self.index).zfill(2))
        Image.fromarray(self.output_image).save(save_path + '.tif')
