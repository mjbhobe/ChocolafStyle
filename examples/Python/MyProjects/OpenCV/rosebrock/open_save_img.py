#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* open_save_img.py - open & save images with OpenCV
*
* @author: Manish Bhobe
* My experiments with Python, C++, OpenCV, Data Science & ML
* Code is provided for learning purposes only! Use at your own risk!!
"""
import os
import sys
import pathlib
from argparse import ArgumentParser

import numpy as np
import cv2
import cv2_utils
from cv2_utils import cv2_imshow, cv2_imread_from_url

IMAGES_PATH = pathlib.Path(__file__).parent.parent / "images"
DEFAULT_IMAGE = IMAGES_PATH.joinpath("cat-1.jpg")


def main():
    assert DEFAULT_IMAGE.exists(), f"FATAL ERROR: cannot find {DEFAULT_IMAGE}"
    ap = ArgumentParser()
    ap.add_argument("-i", "--image", help="Full path to image")
    args = vars(ap.parse_args())

    # read in the image
    image_path = str(DEFAULT_IMAGE)
    if args["image"]:
        assert os.path.exists(args["image"])
        image_path = args["image"]

    image_name = os.path.basename(image_path)

    # open image as colored (RGB image)
    print(f"Opening {image_path}")
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # display some info on image
    h, w, c = image.shape
    print(f"Image dims -> h: {h} pix - w: {w} pix - c: {c} channels", flush=True)

    cv2_imshow(image, title=f"Image: {image_name}")

    # convert color spaces
    image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    cv2_imshow(image_yuv, f"Image: {image_name} (YUV Colorspace)")

    # open image as grayscale
    image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    cv2_imshow(image_gray, f"Image: {image_name} (gray-scale)")

    # translate image by 70, 110
    cx, cy = 70, 110
    translated_image = cv2_utils.translate_image(image, cx, cy)
    cv2_imshow(translated_image, f"Image translated by ({cx}, {cy})")

    degrees = 45
    num_rows, num_cols = image.shape[:2]
    rotated_image = cv2_utils.rotate_image(image, degrees)
    cv2_imshow(
        rotated_image,
        f"Image rotated by {degrees} about ({num_cols // 2}, {num_rows // 2})",
    )

    center_x, center_y = num_cols // 3, num_rows // 4
    scale_factor = 0.75
    rotated_image = cv2_utils.rotate_image(
        image, degrees, scale_factor=scale_factor, cx=center_x, cy=center_y
    )
    title = f"Image rotated by {degrees} about ({center_x}, {center_y}) with scale-factor {scale_factor}"
    cv2_imshow(rotated_image, title)

    scalex, scaley = 1.2, 0.8
    scaled_image = cv2_utils.scale_image(
        image, scalex, scaley, interpolation=cv2.INTER_LINEAR
    )
    cv2_imshow(scaled_image, f"Scaling ({scalex}, {scaley}) - Linear Interpolation")
    scaled_image = cv2_utils.scale_image(
        image, scalex, scaley, interpolation=cv2.INTER_CUBIC
    )
    cv2_imshow(scaled_image, f"Scaling ({scalex}, {scaley}) - Cubic interpolation")

    # now let's set top left rectangle to blue
    h, w, c = image.shape
    # note OpenCV sets colors as BRG not RGB, so blue is (255,0,0) & not (0,0,255)
    image[: h // 4, : w // 4, :] = (255, 0, 0)
    cv2_imshow(image, title=f"Blue Image: {image_name}")

    # np.random.sample()


if __name__ == "__main__":
    main()
