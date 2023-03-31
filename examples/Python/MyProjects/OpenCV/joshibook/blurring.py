#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* wavelets.py - wave effects with OpenCV
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
    sharp_edges_image_path = IMAGES_PATH.joinpath("sharp_edges.png")
    sharp_edges_image = cv2.imread(str(sharp_edges_image_path), cv2.IMREAD_COLOR)
    num_rows, num_cols = sharp_edges_image.shape[:2]

    # blur kernels
    kernel_identity = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    kernel_3x3 = np.ones((3, 3), np.float32) / 9.0
    kernel_5x5 = np.ones((5, 5), np.float32) / 25.0
    kernel_7x7 = np.ones((7, 7), np.float32) / 49.0
    kernel_15x15 = np.ones((15, 15), np.float32) / (15.0 * 15.0)

    sharp_edges_identity = cv2.filter2D(sharp_edges_image, -1, kernel_identity)
    sharp_edges_3x3 = cv2.filter2D(sharp_edges_image, -1, kernel_3x3)
    sharp_edges_5x5 = cv2.filter2D(sharp_edges_image, -1, kernel_5x5)
    sharp_edges_7x7 = cv2.filter2D(sharp_edges_image, -1, kernel_7x7)
    sharp_edges_15x15 = cv2.filter2D(sharp_edges_image, -1, kernel_15x15)
    sharp_edges_blur = cv2.blur(sharp_edges_image, (15, 15))

    cv2_imxshow(
        [sharp_edges_image, sharp_edges_identity, sharp_edges_3x3, sharp_edges_5x5, sharp_edges_7x7,
         sharp_edges_15x15, sharp_edges_blur],
        ["Original", "Identity Filter", "3x3 Filter", "5x5 Filter", "7x7 Filter", "15x15 Filter",
         "Blur Effect"],
        title = "Blur Effects",
        fig_size = (16, 3),
        max_cols = 10
    )


if __name__ == "__main__":
    main()
