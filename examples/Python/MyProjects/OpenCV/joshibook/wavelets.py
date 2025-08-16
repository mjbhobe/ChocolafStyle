#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* wavelets.py - wave effects with OpenCV
*
* @author: Manish Bhobé
* My experiments with Python, C++, OpenCV, Data Science & ML
* Code is provided for learning purposes only! Use at your own risk!!
"""
import sys, os
import math
import pathlib

import numpy as np
import cv2

# add our module to sys.path
UTILS_PATH = pathlib.Path(__file__).parent.parent
sys.path.append(str(UTILS_PATH))

import cv2_utils
from cv2_utils import cv2_imxshow

IMAGES_PATH = pathlib.Path(__file__).parent.parent / "images"


def main():
    manish_image_path = IMAGES_PATH.joinpath("manish.png")
    manish_image = cv2.imread(str(manish_image_path), cv2.IMREAD_COLOR)
    num_rows, num_cols = manish_image.shape[:2]

    # verticle wave
    manish_vw = np.zeros(manish_image.shape, dtype=manish_image.dtype)
    for i in range(num_rows):
        for j in range(num_cols):
            offset_x = int(25.0 * math.sin(2 * math.pi * i / 180))
            offset_y = 0
            if j + offset_x < num_rows:
                manish_vw[i, j] = manish_image[i, (j + offset_x) % num_cols]
            else:
                manish_vw[i, j] = 0

    # horizontal wave
    manish_hw = np.zeros(manish_image.shape, dtype=manish_image.dtype)
    for i in range(num_rows):
        for j in range(num_cols):
            offset_x = 0
            offset_y = int(16.0 * math.sin(2 * math.pi * j / 150))
            if i + offset_y < num_rows:
                manish_hw[i, j] = manish_image[(i + offset_y) % num_rows, j]
            else:
                manish_hw[i, j] = 0

    # both effects
    manish_both = np.zeros(manish_image.shape, dtype=manish_image.dtype)
    for i in range(num_rows):
        for j in range(num_cols):
            offset_x = int(20.0 * math.sin(2 * 3.14 * i / 150))
            offset_y = int(20.0 * math.cos(2 * 3.14 * j / 150))
            if i + offset_y < num_rows and j + offset_x < num_cols:
                manish_both[i, j] = manish_image[
                    (i + offset_y) % num_rows, (j + offset_x) % num_cols
                ]
            else:
                manish_both[i, j] = 0

    cv2_imxshow(
        [manish_image, manish_vw, manish_hw, manish_both],
        ["Original", "Vertical Wave", "Horizontal Wave", "Both"],
        title="Wave effects",
        fig_size=(12, 6),
    )


if __name__ == "__main__":
    main()
