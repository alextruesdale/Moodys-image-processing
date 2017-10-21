"""Top-level project Main function."""

import ImageReader
import ImageOperator

def main():
    """Read file directory images and the run the Image Operator aggregate function."""

    files = ImageReader.file_read_operate()
    for file in files:
        print(file)
        ImageOperator.ImageOperator(file)

if __name__ == "__main__":
    main()
