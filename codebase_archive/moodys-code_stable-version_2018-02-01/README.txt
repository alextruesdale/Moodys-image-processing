features
--------
- horizontal cropping of appropriate images
- vertical cropping of 2 and 3 columns images
- saves in aggregate format by fiche. All images in a fiche are saved in a single folder, named by image #
- oct-ready images are marked as such to be pulled

new
---

- Temporary suspension of ‘meta_read’ function
- Additional side trimming to account for darker images
- Tweaked parameters for:
  - ‘ImageRotater’: degrees of rotation, whiteness quantity req’d
  - ’ImageCropper’: added trimming run with guardrails to keep from cropping too far
  - ‘ImageColumnCropOperators’: modified vertical ‘list_clean’ parameters (more loose)
  - ’ImageVerticalCrop’: expanded mathematical column boundaries, modified cleaning parameters (more loose)
 
