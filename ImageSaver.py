"""ImageSaver module; imported by ImageOperate aggregate class."""

import json
import os
from PIL import Image

class ImageSaver(object):

    """
    The column cropping function to be applied to each image, dynamically splitting it
    on vertical columns.

    Attributes:
        file: Path of file in original directory.
        output_images: Incoming tuple of output image arrays to be written as images, saved.
        number_columns: Incoming string indicating where final images will be saved.
        meta_variables: Incoming dictionary of meta information of image.
        save_folder: Path of save folder for instance image.
    """

    def __init__(self, file, image_to_columns, image_meta_data):

        self.file = file
        self.output_images = image_to_columns.output_images
        self.column_folder = image_to_columns.number_columns
        self.meta_variables = image_meta_data.meta_variables
        self.save_folder = self.image_save()

        self.json_write()

    def image_save(self):
        """Write image arrays as images and save them into the correct save folder."""

        # Define dynamic save variables from original file path.
        flexible_directory = ('output/' + os.path.dirname(self.file).split('/')[-2] + '/' +
                              os.path.dirname(self.file).split('/')[-1] + '/')

        base = os.path.basename(os.path.splitext(os.path.basename(self.file))[0])

        # Create image save folder.
        working_directory = os.getcwd()
        save_folder = os.path.join(working_directory  + '/' + flexible_directory +
                                   self.column_folder + base)

        os.makedirs(save_folder)

        # Save full image and page number crop.
        Image.fromarray(self.output_images[0]).save(os.path.join(save_folder, 'full_image_' +
                                                                 os.path.basename(self.file)))

        Image.fromarray(self.output_images[1]).save(os.path.join(save_folder, 'page_number_' +
                                                                 os.path.basename(self.file)))

        # Save cropped columns (accounts for single column images).
        i = 1
        if len(self.output_images) > 2:
            for image in self.output_images[2:]:
                cut = ('cut' + str(i) + '_')
                Image.fromarray(image).save(os.path.join(save_folder, cut +
                                                         os.path.basename(self.file)))
                i += 1

        return save_folder

    def json_write(self):
        """Write meta information to JSON output file."""

        with open(os.path.join(self.save_folder, 'meta_information.json'), 'w') as output:
            json.dump(self.meta_variables, output, sort_keys=True, indent=3)
