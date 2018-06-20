"""Static operators for xml parsing."""

import os

def clear_destination(file_path):
    """Identify if file exists. If so, remove it."""

    if os.path.exists(file_path):
        os.remove(file_path)
