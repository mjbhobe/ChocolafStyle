import sys
import pathlib
import numpy as np
import cv2


# add our module to sys.path
UTILS_PATH = pathlib.Path(__file__).parent.parent
sys.path.append(str(UTILS_PATH))

from cv2_utils import cv2_imshow, cv2_imread_from_url


URL = "http://s0.geograph.org.uk/photos/40/57/405725_b17937da.jpg"
PIXABAY_URL = "https://pixabay.com/photos/oil-abstract-bubble-background-6915740/oil-6915740_1280.jpg"


def main():
    img = cv2_imread_from_url(PIXABAY_URL)
    cv2_imshow(img, f"Image from URL\n{PIXABAY_URL}")


if __name__ == "__main__":
    main()
