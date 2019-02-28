<img src = "https://github.com/alextruesdale/moodys-image-processing/blob/master/repository_media/1940_plots_11.png" alt = "1940_plots_11" title = "1940_plots_11" align = "right" height = "225" />

# Python Image Processing – Moody's Industry Data
There are ~500,000 documents in the Moody's industry data archive recorded during the 20th century on paper prior to digital data storage. This suite of tools prepares scanned .tif images to be read by OCR software (OmniPage), following which, page data is analysed at the text level to determine OCR error and section breaks for extracting structure information from the scans.

This project continues at the Leeds School of Business at the University of Colorado, Boulder. The contents of this repository are the WIP tools that I created whilst working of the research team.

Object Oriented Tools manage the following tasks:
- Dynamically correct for image scanning errors (rotation, cropping)
- Manually zone text and tables using OCR XML and text output
- Organise and analyse unstructured / error-prone OCR text output

## Example Input
<img src = "https://github.com/alextruesdale/moodys-image-processing/blob/master/repository_media/Banks19380027-0070.png" alt = "1940_plots_11" title = "1940_plots_11" align = "center" width = "850" />
