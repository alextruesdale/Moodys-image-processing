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

    if exin == 'exclude':
        # Set source and destination for directory copy function.
        source = (os.path.join(os.getcwd()))
        destination = (os.path.join(os.getcwd(), pathname))

        def ignore_files(directory, files):
            """Ignore files when copying directory tree"""

            return [file for file in files if os.path.isfile(os.path.join(directory, file))]

        # Copy directory into 'output' folder.
        if os.path.exists(os.path.join(os.getcwd(), pathname)):
            shutil.rmtree(os.path.join(os.getcwd(), pathname))

        shutil.copytree(source, destination, ignore=ignore_files)

    # Return list of file paths
    return files

### Create Final Directories

def final_directories():
    """Create final directories in each subdirectory of output directory"""

    # Define output directory and sub-directories for sort images by #columns.
    output_directory = (os.path.join(os.getcwd(), 'output'))
    save_directories = ['one-column', 'two-column', 'three-column', 'bin']

    # Populate 3rd-level sub-directories (two level within 'output') with save_directories folders.
    for item in os.listdir(output_directory):
        sub = (os.path.join(os.getcwd(), 'output', item))

        for directory in os.listdir(sub):
            for sub_directory in save_directories:
                os.makedirs(sub + '/' + directory + '/' + sub_directory)

def file_read_operate(exin, pathname):
    """Aggregate function triggering read_files & final_directories"""

    files = read_files(exin, pathname)
    final_directories()

    # Return list of file paths
    return files
