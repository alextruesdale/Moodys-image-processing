# Image Processing Tool – Moody's Industry Data
This is a WIP Repository displaying code written for the Leeds School of Business NLP Lab by Alex Truesdale.

There are ~500,000 documents in the Moody's industry data archive recorded on paper during the 20th century prior to digital data storage. This tool prepares raw .tif images to be read by OCR software, following which page data can be stored in a queryable database.

While these operations carried out on an individual image are simple, preparing the functions to run flexibly at scale adds additional layers of complexity.
<br><br>

## Operations
#### Rotate
The workflow first rotates the image, testing for the greatest amount of vertical whitespace.

#### Initial Crop
The straightened image is cropped in to the page itself, removing black borders.
<img src="https://github.com/alextruesdale/moodys-image-processing/blob/master/repository_media/Inital_Crop.png" alt="Gulp Demo" title="Alex Truesdale" align="center" width="97%" />

#### Column Crop
The cropped image is searched for columns and then cropped on those points (if more than 2 columns).

<br>
<img src="https://github.com/alextruesdale/moodys-image-processing/blob/master/repository_media/Column_Crop.png" alt="Gulp Demo" title="Alex Truesdale" align="center" width="97%" />

#### Meta Details & Save
File and image details are parsed/extracted and saved as a JSON file; images in the list of cropped image arrays are saved and organised following the incoming file structure.
