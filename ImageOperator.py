"""ImageOperator module called by Main function."""

import ImageRotater
import ImageCropper
import ImageColumnCropper
import ImageSaver
import ImageMetaRead

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

    def __init__(self, file):

        self.file = file
        self.rotated_image = ImageRotater.ImageRotater(self.file)
        self.cropped_image_full = ImageCropper.ImageCropper(self.rotated_image)
        self.image_to_columns = ImageColumnCropper.ImageColumnCropper(self.cropped_image_full)
        self.image_meta_data = ImageMetaRead.ImageMetaRead(self.file, self.cropped_image_full,
                                                           self.image_to_columns)

        self.save_images = ImageSaver.ImageSaver(self.file, self.image_to_columns,
                                                 self.image_meta_data)
