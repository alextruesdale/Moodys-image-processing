"""ImageColumnCropOperators module; imported by ImageOperate aggregate class."""

import pandas as pd

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
