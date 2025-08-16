#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* hellocv2.py - hello OpenCV - open & show an image.
*
* @author: Manish Bhobé
* My experiments with Python, C++, OpenCV, Data Science & ML
* Code is provided for learning purposes only! Use at your own risk!!
"""
import sys
import os
import pathlib

import numpy as np
import cv2

# add cv2_utils to sys.path
UTILS_PATH = pathlib.Path(__file__).parent.parent
sys.path.append(str(UTILS_PATH))

import cv2_utils
from cv2_utils import cv2_imshow

IMAGES_PATH = pathlib.Path(__file__).parent.parent / "images"
DEFAULT_IMAGE = IMAGES_PATH.joinpath("curious_muffin.jpg")

image = cv2.imread(str(DEFAULT_IMAGE))
if image is None:
    print(f"Unable to open image {str(DEFAULT_IMAGE)}")
    sys.exit(-1)
else:
    cv2_imshow(image)
