#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* affines.py - affine transforms on images
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
DEFAULT_IMAGE = IMAGES_PATH.joinpath("cat-1.jpg")


def main():
    manish_image_path = IMAGES_PATH.joinpath("manish.png")
    manish_image = cv2.imread(str(manish_image_path), cv2.IMREAD_COLOR)

    num_rows, num_cols = manish_image.shape[:2]
    src_points = np.float32([[0, 0], [num_cols - 1, 0], [0, num_rows - 1]])
    dst_points = np.float32(
        [[0, 0], [int(0.6 * (num_cols - 1)), 0], [int(0.4 * (num_cols - 1)), num_rows - 1]]
    )
    manish2 = cv2_utils.affine_transform_image(manish_image, src_points, dst_points)
    cv2_imxshow(
        [manish_image, manish2], ["Your's Truly", "All scrunched up!"],
        title = "Affine Transform"
    )

    # flip manish
    src_points = np.float32([[0, 0], [num_cols - 1, 0], [0, num_rows - 1]])
    dst_points = np.float32([[num_cols - 1, 0], [0, 0], [num_cols - 1, num_rows - 1]])
    manish_flipped = cv2_utils.affine_transform_image(manish_image, src_points, dst_points)
    cv2_imxshow(
        [manish_image, manish_flipped], ["Original", "Flipped?"], title = "Flipping about Y"
    )

    # perspective transformation
    src_points = np.float32([[0, 0], [num_cols - 1, 0], [0, num_rows - 1], [num_cols - 1, num_rows - 1]])
    dst_points = np.float32(
        [[0, 0], [num_cols - 1, 0], [int(0.33 * num_cols), num_rows - 1],
         [int(0.66 * num_cols), num_rows - 1]]
    )
    manish_cone = cv2_utils.perspective_transform_image(manish_image, src_points, dst_points)
    cv2_imxshow(
        [manish_image, manish_cone], ["Original", "Conical?"], title = "Perspective Transformation"
    )

    # # now let's set top left rectangle to blue
    # h, w, c = image.shape
    # # note OpenCV sets colors as BRG not RGB, so blue is (255,0,0) & not (0,0,255)
    # image[:h // 4, :w // 4, :] = (255, 0, 0)
    # cv2_imshow(image, title = f"Blue Image: {image_name}")

    # np.random.sample()


if __name__ == "__main__":
    main()
