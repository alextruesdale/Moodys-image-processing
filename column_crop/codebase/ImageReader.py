"""ImageReader module; imported by ImageOperate aggregate class."""

import os
import shutil

"""
Image reader function that detects all source images and prepares the export directory.
Returns list of all .tif files in project directory and builds 'output' folder and sub-folders.
"""

def read_files(exin, pathname):
    """Walk through subdirectories and build list of all .tif files"""

    files = []
    # Searches subdirectories within current directory for all .tif files.

    for path, dirnames, filenames in os.walk(os.getcwd()):
        for filename in filenames:
            if exin == 'include':
                if pathname in path:
                    file = os.path.join(path, filename)
                    if 'column' in file:
                        print(file)
                        os.remove(file)

    for path, dirnames, filenames in os.walk(os.getcwd()):
        for filename in filenames:
            if exin == 'exclude':
                if pathname not in path:
                    if filename.endswith('.tif'):
                        file = os.path.join(path, filename)
                        files.append(file)
            elif exin == 'include':
                if pathname in path:
                    if filename.endswith('.tif') and 'column' not in filename:
                        file = os.path.join(path, filename)
                        files.append(file)

    files = sorted(files)
    return files
