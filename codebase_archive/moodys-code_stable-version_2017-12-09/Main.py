"""Top-level project Main function."""

import time
import logging
import ImageReader
import ImageOperator
logging.basicConfig(filename='RuntimeErrors.log', filemode='w', level=logging.ERROR)
logger = logging.getLogger(__name__)

def main():
    """Read file directory images and the run the Image Operator aggregate function."""

    files = ImageReader.file_read_operate('exclude', 'output')
    for file in files:

        start_time = time.time()
        print(file)
        try:
            ImageOperator.ImageOperator(file)
        except Exception as e:
            logger.error('\n\n' + 'File: ' + file + '\n' + 'Error Message: ' +
                         str(e), exc_info=True)

        elapsed_time = round(time.time() - start_time, 2)
        print('Duration:', str(elapsed_time) + ' seconds')


if __name__ == "__main__":
    main()
