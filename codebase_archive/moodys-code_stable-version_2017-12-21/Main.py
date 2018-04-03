"""Top-level project Main function."""

import time
import logging
import numpy as np
import ImageReader
import ImageOperator

logging.basicConfig(filename='RuntimeErrors.log', filemode='w', level=logging.ERROR)
logger = logging.getLogger(__name__)

def main():
    """Read file directory images and the run the Image Operator aggregate function."""

    files = ImageReader.file_read_operate('exclude', 'output')
    job_times = []
    job_time = 0
    files_operated = 0
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

        job_times.append(elapsed_time)
        job_time += elapsed_time
        files_operated += 1

    print('')
    print('job time:', round(job_time, 2), 'seconds', '...', round((job_time / 60), 3), 'minutes')
    print('average job time:', round(np.mean(job_times), 3), 'seconds')
    print('images operated:', files_operated)

if __name__ == "__main__":
    main()
