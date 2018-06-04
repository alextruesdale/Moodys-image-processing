"""ImageSaver module; imported by ImageOperate aggregate class."""

import os
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

    def __init__(self, file_input, image_input):

        self.file = file_input
        self.output_image = image_input.final_cropped_array
        self.save_folder = self.image_save()

    def image_save(self):
        """Write image arrays as images and save them into the correct save folder."""

        # Define dynamic save variables from original file path.
        flexible_directory = ('/output/' + os.path.dirname(self.file).split('/')[-1])

        # Create image save folder.
        working_directory = os.getcwd()
        save_folder = os.path.join(working_directory + flexible_directory)

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Save full image.
        Image.fromarray(self.output_image).save(os.path.join(save_folder, (os.path.basename(self.file)[:-4] + '.tif')))
        return save_folder
