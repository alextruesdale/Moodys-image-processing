"""ImageOperator module called by Main function."""

from ImageRotater import ImageRotater
from ImageCropper import ImageCropper
from ImageSaver import ImageSaver

class ImageOperator(object):

    """
    Aggregate operator function; performs rotation, cropping, column cropping, and saving functions.

    Attributes:
        file: Path of file in original directory.
        rotated_image: Resulting instance of ImageRotater class.
        cropped_image_full: Resulting instance of ImageCropper class.
        save_images: Resulting instance of ImageSaver class.
    """

    def __init__(self, file):

        self.file = file
        self.rotated_image = ImageRotater(self.file)
        self.cropped_image_full = ImageCropper(self.rotated_image)
        self.save_images = ImageSaver(self.file,
                                      self.cropped_image_full)
