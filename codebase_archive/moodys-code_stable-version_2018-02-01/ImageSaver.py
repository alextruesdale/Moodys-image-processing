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
        meta_variables: Incoming dictionary of meta information of image.
        save_folder: Path of save folder for instance image.
    """

    def __init__(self, file, image_input):
                           # , image_meta_data)

        self.file = file
        self.horizontal_ocr = image_input.horizontal_ocr_list
        self.output_images = image_input.output_images
        # self.meta_variables = image_meta_data.meta_variables
        self.save_folder = self.image_save()

        self.json_write()

    def image_save(self):
        """Write image arrays as images and save them into the correct save folder."""

        # Define dynamic save variables from original file path.
        flexible_directory = ('/output/' + os.path.dirname(self.file).split('/')[-1])

        base = os.path.basename(os.path.splitext(os.path.basename(self.file))[0])

        # Create image save folder.
        working_directory = os.getcwd()
        save_folder = os.path.join(working_directory + flexible_directory)

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Save page number crop.
        Image.fromarray(self.output_images[0]).save(os.path.join(save_folder, os.path.basename(self.file)[:-4] + '_page_number' + '.tif'))

        # Save full image.
        Image.fromarray(self.output_images[1]).save(os.path.join(save_folder, os.path.basename(self.file)[:-4] + '_full_image' + '.tif'))

        # Save horizontal cropped images.
        key_list = []
        for i, value in enumerate(self.horizontal_ocr):
            if value == 1:
                key_list.append(i)

        i = 1
        for image in self.output_images[2]:
            count = str(i).zfill(2)

            if i-1 in key_list:
                Image.fromarray(image).save(os.path.join(save_folder, os.path.basename(self.file)[:-4] + '_ocr_horizontal_cut_' + count + '.tif'))
            else:
                Image.fromarray(image).save(os.path.join(save_folder, os.path.basename(self.file)[:-4] + '_horizontal_cut_' + count + '.tif'))
            i += 1

        # Save vertical cropped images.
        i = 1
        if len(self.output_images) > 3:
            for image in self.output_images[3][::-1]:
                count = str(i).zfill(2)

                Image.fromarray(image).save(os.path.join(save_folder, os.path.basename(self.file)[:-4] + '_ocr_vertical_cut_' + count + '.tif'))
                i += 1

        return save_folder

    # def json_write(self):
    #     """Write meta information to JSON output file."""
    #
    #     with open(os.path.join(self.save_folder, 'meta_information.json'), 'w') as output:
    #         json.dump(self.meta_variables, output, sort_keys=True, indent=3)
