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
            if exin == 'exclude':
                if pathname not in path:
                    if filename.endswith('.tif'):
                        file = os.path.join(path, filename)
                        files.append(file)
            else:
                if pathname in path:
                    if filename.endswith('.tif'):
                        file = os.path.join(path, filename)
                        files.append(file)

    return files

### Create Final Directories

def final_directories():
    """Create final directories in each subdirectory of output directory"""

    # Define and create output directory for sort images.
    output_directory = (os.path.join(os.getcwd(), 'output'))

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    else:
        shutil.rmtree(output_directory)
        os.mkdir(output_directory)

def file_read_operate(exin, pathname):
    """Aggregate function triggering read_files & final_directories"""

    files = read_files(exin, pathname)
    final_directories()

    # Return list of file paths
    return files
