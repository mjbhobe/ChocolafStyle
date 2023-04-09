#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* edge_detection.py - applying various edge detection alogorithms
*
* @author: Manish Bhobe
* My experiments with Python, C++, OpenCV, Data Science & ML
* Code is provided for learning purposes only! Use at your own risk!!
"""
import sys, os
import pathlib

import cv2

# add our module to sys.path
UTILS_PATH = pathlib.Path(__file__).parent.parent
sys.path.append(str(UTILS_PATH))

import cv2_utils
from cv2_utils import cv2_imxshow

IMAGES_PATH = pathlib.Path(__file__).parent.parent / "images"


def main():
    geom_inputs_image_path = IMAGES_PATH.joinpath("geometrics_input.png")
    geom_inputs_image = cv2.imread(str(geom_inputs_image_path), cv2.IMREAD_GRAYSCALE)
    print(type(geom_inputs_image))
    num_rows, num_cols = geom_inputs_image.shape[:2]

    # let's apply filters
    sobel_horz = cv2.Sobel(geom_inputs_image, cv2.CV_64F, 1, 0, ksize = 5)
    sobel_vert = cv2.Sobel(geom_inputs_image, cv2.CV_64F, 0, 1, ksize = 5)
    laplacian = cv2.Laplacian(geom_inputs_image, cv2.CV_64F)
    canny = cv2.Canny(geom_inputs_image, 50, 240)

    cv2_imxshow(
        [geom_inputs_image, sobel_horz, sobel_vert, laplacian, canny],
        ["Original", "Sobel Horizontal", "Sobel Vertical", "Laplacian", "Canny"],
        title = "Edge Detection",
        fig_size = (16, 5),
        apply_cvt = False
    )


if __name__ == "__main__":
    main()
