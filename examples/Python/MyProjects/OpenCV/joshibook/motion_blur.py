#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* motion_blur.py: apply motion blur, so it appears that you are viewing
*   image from a moving vehicle
*
* @author: Manish Bhobe
* My experiments with Python, C++, OpenCV, Data Science & ML
* Code is provided for learning purposes only! Use at your own risk!!
"""
import sys, os
import pathlib

import numpy as np
import cv2

# add our module to sys.path
UTILS_PATH = pathlib.Path(os.getcwd()).parent
sys.path.append(str(UTILS_PATH))

import cv2_utils
from cv2_utils import cv2_imxshow

IMAGES_PATH = pathlib.Path(__file__).parent.parent / "images"


def main():
    tree_image_path = IMAGES_PATH.joinpath("tree_input.png")
    tree_image = cv2.imread(str(tree_image_path))
    num_rows, num_cols = tree_image.shape[:2]
    size = 15

    # let's apply filters
    kernel_motion_blur = np.zeros((size, size))
    kernel_motion_blur[int((size - 1) / 2), :] = np.ones(size)
    kernel_motion_blur = kernel_motion_blur / size

    output = cv2.filter2D(tree_image, -1, kernel_motion_blur)

    cv2_imxshow(
        [tree_image, output],
        ["Original", "Motion Blurred"],
        title = "Motion Blur Effect",
        fig_size = (10, 4)
    )

    # sharpening image
    kernel_sharpen_1 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    kernel_sharpen_2 = np.array([[1, 1, 1], [1, -7, 1], [1, 1, 1]])
    kernel_sharpen_3 = np.array(
        [
            [-1, -1, -1, -1, -1],
            [-1, 2, 2, 2, -1],
            [-1, 2, 8, 2, -1],
            [-1, 2, 2, 2, -1],
            [-1, -1, -1, -1, -1]
        ]
    ) / 8.0

    # applying different kernels to the input image
    output_1 = cv2.filter2D(tree_image, -1, kernel_sharpen_1)
    output_2 = cv2.filter2D(tree_image, -1, kernel_sharpen_2)
    output_3 = cv2.filter2D(tree_image, -1, kernel_sharpen_3)

    cv2_imxshow(
        [tree_image, output_1, output_2, output_3],
        title = "Sharpening Effect",
        fig_size = (10, 8),
        max_cols = 2
    )


if __name__ == "__main__":
    main()
