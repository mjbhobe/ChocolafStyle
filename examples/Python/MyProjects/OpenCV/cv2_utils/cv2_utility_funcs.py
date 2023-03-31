# -*- coding: utf-8 -*-

"""
* cv2_utility_funcs.py - OpenCV utilities for images
*
* @author: Manish Bhobe
* My experiments with Python, C++, OpenCV, Data Science & ML
* Code is provided for learning purposes only! Use at your own risk!!
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List


def cv2_imshow(img, title = None, fig_size = None, show_axis = False):
    """ show cv2 image in a matplotlib plot output window """
    # convert from default BGR to RGB schema
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if fig_size is not None:
        plt.figure(figsize = fig_size)
    if title is not None:
        plt.title(title)
    if not show_axis:
        plt.axis('off')
    plt.imshow(image, cmap = "Greys")
    plt.show()


def cv2_imxshow(
    images: List[np.ndarray], titles: List[str] = None, title = None, fig_size = None, show_axis = False,
    max_cols = 5, apply_cvt = True
) -> None:
    """ shows a list of images in the same matplotlib window """
    if titles is not None:
        assert len(images) == len(titles), \
            f"FATAL ERROR: number of titles should be same as number of images!"

    num_images = len(images)
    num_cols = max_cols if num_images > max_cols else num_images
    num_rows = num_images // max_cols
    num_rows += 1 if num_images % max_cols > 0 else 0

    f, ax = plt.subplots(num_rows, num_cols, figsize = fig_size)
    f.tight_layout()
    f.subplots_adjust(top = 0.90)

    for row in range(num_rows):
        for col in range(num_cols):
            index = row * num_cols + col
            image = images[index]
            if apply_cvt:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if index < num_images:
                if num_rows > 1:
                    ax[row, col].axis("off")
                    ax[row, col].imshow(image, cmap = "Greys")
                    if titles is not None:
                        ax[row, col].set_title(titles[index])
                else:
                    ax[col].axis("off")
                    ax[col].imshow(image, cmap = "Greys")
                    if titles is not None:
                        ax[col].set_title(titles[index])

    if title is not None:
        plt.suptitle(title)
    plt.show()


def translate_image(image: np.ndarray, cx: int, cy: int) -> np.ndarray:
    """ translates an image by cx & cy pixels in x & y direction
        apples translation matrix
            | 1 0 cx |
            | 0 1 cy |
        to translate the image by cx & cy pixels
    """
    num_rows, num_cols = image.shape[:2]
    translation_matrix = np.array([[1, 0, cx], [0, 1, cy]]).astype(np.float32)
    image_translated = cv2.warpAffine(image, translation_matrix, (num_cols + cx, num_rows + cy))
    return image_translated


def rotate_image(
    image: np.ndarray, angle_degrees: int, scale_factor: float = 1.0, cx: int = None, cy: int = None
) -> np.ndarray:
    """ rotates images by angle_degrees in degrees about point cx, cy (if specified)"""
    num_rows, num_cols = image.shape[:2]
    cx_rotate = num_cols // 2 if cx is None else cx
    cy_rotate = num_rows // 2 if cy is None else cy
    rotation_matrix = cv2.getRotationMatrix2D((cx_rotate, cy_rotate), angle_degrees, scale_factor)
    image_rotated = cv2.warpAffine(image, rotation_matrix, (num_cols, num_rows))
    return image_rotated


def scale_image(
    image: np.ndarray, scalex: float, scaley: float, interpolation = cv2.INTER_LINEAR
) -> np.ndarray:
    """ scales an image by scalex & scaley (floats) where 1.0 = 100% """
    image_scaled = cv2.resize(image, None, fx = scalex, fy = scaley, interpolation = interpolation)
    return image_scaled


def affine_transform_image(
    image: np.ndarray, src_points: np.ndarray, dst_points: np.ndarray
) -> np.ndarray:
    """ applies generic affine transform about src & dst points"""
    assert src_points.shape == dst_points.shape, "FATAL: point shapes do not match!"

    num_rows, num_cols = image.shape[:2]
    affine_matrix = cv2.getAffineTransform(src_points, dst_points)
    image_transformed = cv2.warpAffine(image, affine_matrix, (num_cols, num_rows))
    return image_transformed


def perspective_transform_image(
    image: np.ndarray, src_points: np.ndarray, dst_points: np.ndarray
) -> np.ndarray:
    """ applies perspective transform to image using source & dest points arrays"""
    assert src_points.shape == dst_points.shape, "FATAL: point shapes do not match!"

    num_rows, num_cols = image.shape[:2]
    perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    image_transformed = cv2.warpPerspective(image, perspective_matrix, (num_cols, num_rows))
    return image_transformed
