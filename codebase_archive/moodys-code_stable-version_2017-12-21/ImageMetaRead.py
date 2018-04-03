"""ImageMetaRead module; imported by ImageOperate aggregate class."""

import os
import re
from PIL import Image

class ImageMetaRead(object):

    """
    Metadata collection function do derive organisational data from each image; saved as

    Attributes:
        image_column_data: Incoming string denoting number of columns in the image.
        full_image_array: Incoming array of the final cropped image.

        image_path: Full image path.
        image_id: Image ID (e.g. B28_V0_11_07) Industry ID, Year, Volume, Collection, Image Number.
        image_dimensions: Length measure of horizontal and vertical axes (e.g. (3054, 4132)).
        industry: Image industry (taken from image_path).
        industry_id: ID based on industry.
        year: Image year (taken from image_path).
        volume: Image volume (taken from image_path).
    """

    def __init__(self, file, cropped_image_full, image_input):

        self.full_image_array = cropped_image_full.final_cropped_array

        self.image_path = os.path.abspath(os.path.join(os.pardir, file))
        self.file_path = self.image_path.split('/')[-1]
        self.image_id = self.set_image_id()
        self.image_dimensions = self.set_image_dimensions()
        self.industry = self.set_industry()
        self.industry_id = self.set_industry_id()
        self.year = self.set_year()
        self.volume = self.set_volume()
        self.meta_variables = self.return_meta_variables()

    def set_image_id(self):
        """Prepare Image ID."""

        #RegEx functions to extract relevant data.
        id_components1 = re.search(r'(^\w)\w+19(\d{2}).*00(\d{2}).*00(\d{2})', self.file_path)
        id_components2 = re.search(r'.*(V)\w+\.(\d).*', self.file_path)

        if id_components2:
            image_id = (id_components1.group(1) + id_components1.group(2) + '_' +
                        id_components2.group(1) + id_components2.group(2) + '_' +
                        id_components1.group(3) + '_' + id_components1.group(4))
        else:
            image_id = (id_components1.group(1) + id_components1.group(2) + '_' + 'V0' + '_'+
                        id_components1.group(3) + '_' + id_components1.group(4))

        return image_id

    def set_image_dimensions(self):
        """Define Image Dimentions."""

        dimensions = (Image.fromarray(self.full_image_array)).size
        return dimensions

    def set_industry(self):
        """Extract Industry name."""

        #RegEx function to extract industry string at beginning of file path.
        industry = re.search(r'(^\w+)19', self.file_path).group(1)
        return industry

    def set_industry_id(self):
        """Encode Industry ID."""

        #RegEx function to extract first letter of industry string.
        industry_id = re.search(r'(^\w{1})', self.file_path).group(1)
        return industry_id

    def set_year(self):
        """Extract Year information."""

        #RegEx function to extract four-digit year (assumes all years in study are in the 1900s).
        year = re.search(r'^\w+(19\d{2})', self.file_path).group(1)
        return year

    def set_volume(self):
        """Extract Volume information."""

        #RegEx function to extract volume string.
        volume_component = re.search(r'.*(V)\w+\.(\d).*', self.file_path)

        if volume_component:
            volume = str(volume_component.group(1) + volume_component.group(2))
        else: volume = None
        return volume

    def return_meta_variables(self):
        """Summarise meta variables to be sent to JSON write function."""

        meta_variables = {
            'image_path' : self.image_path,
            'image_id' : self.image_id,
            'image_dimensions' : self.image_dimensions,
            'industry' : self.industry,
            'industry_id' : self.industry_id,
            'year' : self.year,
            'volume' : self.volume
        }

        return meta_variables
