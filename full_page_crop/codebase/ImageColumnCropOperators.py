"""ImageColumnCropOperators module; imported by ImageOperate aggregate class."""

import pandas as pd
import numpy as np
from PIL import Image

def open_image(file_path):
    """Open images from 'files' list."""

    img = Image.open(file_path)
    return img

def convert_image_luminance(image):
    """Convert rotated image to luminance array."""

    luminance_img = np.asarray((image).convert('L'))
    return luminance_img

def split_array(rolling_mean, split_val):
    """Crop array to only show edges of image (x-pixels from left & right)."""

    split1 = rolling_mean.iloc[: split_val]
    split2 = rolling_mean.iloc[-(split_val) :]
    split_list = [split1, split2]

    return split_list

def convert_rolling_mean(array, axis, interval, offset):
    """Take rolling mean of image array."""

    if offset == 0:
        axis_rollmean = ((pd.DataFrame(list((array.mean(axis=axis)) / 255)))
                         .rolling(interval).mean())
    else:
        axis_rollmean = ((pd.DataFrame(list((array.mean(axis=axis)) / 255)))
                         .rolling(interval).mean()).iloc[offset : -(offset)]

    axis_rollmean.columns = ['values']
    return axis_rollmean

def convert_rolling_sdev(array, axis, interval, offset):
    """Take rolling sdev of image array."""

    if offset == 0:
        axis_rollsdev = ((pd.DataFrame(list((array.std(axis=axis)) / 255)))
                         .rolling(interval).std())
    else:
        axis_rollsdev = ((pd.DataFrame(list((array.std(axis=axis)) / 255)))
                         .rolling(interval).std()).iloc[offset : -(offset)]

    axis_rollsdev.columns = ['values']
    return axis_rollsdev
