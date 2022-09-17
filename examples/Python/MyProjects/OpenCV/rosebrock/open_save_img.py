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
from argparse import ArgumentParser

import cv2
import matplotlib.pyplot as plt
import numpy as np


def cv2_imshow(img, title=None, fig_size=None, show_grid=False):
    """ show cv2 image in a matplotlib plot output window """
    # convert from default BGR to RGB schema
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if fig_size is not None:
        plt.figure(figsize=fig_size)
    if title is not None:
        plt.title(title)
    if not show_grid:
        plt.axis('off')
    plt.imshow(rgb_img)
    plt.show()


def main():
    ap = ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="Full path to image")
    args = vars(ap.parse_args())

    # read in the image
    if os.path.exists(args["image"]):
        image = cv2.imread(args["image"])

        # display some info on image
        h, w, c = image.shape
        print(f"Image dims -> h: {h} pix - w: {w} pix - c: {c} channels", flush=True)

        # cv2.imshow(f"Image : {args['image']}", image)
        # cv2.waitKey()
        cv2_imshow(image, title=f"Image: {args['image']}")

        # now let's set top left rectangle to blue
        h, w, c = image.shape
        # note OpenCV sets colors as BRG not RGB, so blue is RGB(255,0,0)
        image[:h // 4, :w // 4, :] = (255, 0, 0)
        cv2_imshow(image, title=f"Blue Image: {args['image']}")

        # np.random.sample()
    else:
        print(f"{args['image']} - path does not exist!")


if __name__ == "__main__":
    main()
