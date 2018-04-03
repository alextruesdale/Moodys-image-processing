"""ImageOperator module called by Main function."""

from ImageRotater import ImageRotater
from ImageCropper import ImageCropper
from ImageVerticalCrop import ImageVerticalCrop
from ImageHorizontalCrop import ImageHorizontalCrop
from ImageSaver import ImageSaver
from ImageMetaRead import ImageMetaRead
from PIL import Image

class ImageOperator(object):

    """
    Aggregate operator function; performs rotation, cropping, column cropping, and saving functions.

    Attributes:
        file: Path of file in original directory.
        rotated_image: Resulting instance of ImageRotater class.
        cropped_image_full: Resulting instance of ImageCropper class.
        image_to_columns: Resulting instance of ImageColumnCropper class.
        image_meta_data: Resulting instance of ImageMetaData class.
        save_images: Resulting instance of ImageSaver class.
    """

    def __init__(self, file, files_operated):

        self.file = file
        self.rotated_image = ImageRotater(self.file)
        self.cropped_image_full = ImageCropper(self.rotated_image)
        self.vertical_gutter_test = ImageVerticalCrop(self.rotated_image,
                                                      self.cropped_image_full,
                                                      True)

        self.horizontal_gutter_test = ImageHorizontalCrop(self.rotated_image,
                                                          self.cropped_image_full,
                                                          self.vertical_gutter_test)

        self.image_to_columns = ImageVerticalCrop(self.rotated_image,
                                                  self.horizontal_gutter_test,
                                                  False)

        # self.image_meta_data = ImageMetaRead(self.file,
        #                                      self.cropped_image_full,
        #                                      self.image_to_columns)

        self.save_images = ImageSaver(self.file,
                                      self.image_to_columns)
                                      # self.image_meta_data)
