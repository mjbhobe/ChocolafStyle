import os
import random
import logging
import inspect
from datetime import datetime

import numpy as np

from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *


def seed_all(seed=None):
    # to ensure that you get consistent results across runs & machines
    """seed all random number generators to get consistent results
    across multiple runs ON SAME MACHINE - you may get different results
    on a different machine (architecture) & that is to be expected

    @params:
         - seed (optional): seed value that you choose to see everything. Can be None
           (default value). If None, the code chooses a random uint between np.uint31.min
           & np.unit31.max
     @returns:
         - if parameter seed=None, then function returns the randomly chosen seed, else it
           returns value of the parameter passed to the function
    """
    if seed is None:
        # pick a random uint31 seed
        seed = random.randint(np.iinfo(np.uint31).min, np.iinfo(np.uint32).max)
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    return seed


def enable_hi_dpi() -> None:
    """Allow to HiDPI.
    This function must be set before instantiation of QApplication..
    For Qt6 bindings, HiDPI “just works” without using this function.
    """
    from qtpy.QtCore import Qt
    from qtpy.QtGui import QGuiApplication

    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        QGuiApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)  # type: ignore
    if hasattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
        QGuiApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)  # type: ignore
    if hasattr(Qt, "HighDpiScaleFactorRoundingPolicy"):
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
        QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )


def pointsToPixels(points):
    """
    Converts font size from points to pixels
    NOTE: We know that 1 inch = 96 pixels and 1 inch = 72 points
    Hence, 96 pixels = 72 points
    So, x points = x * 96 / 72 pixels"""
    # default_pix_per_inch = 96 if sys.platform == "win32" else 72
    # default_font_dpi = os.getenv("QT_FONT_DPI", default_pix_per_inch)
    # screenDpi = QGuiApplication.primaryScreen().physicalDotsPerInch()
    # return int((points * default_font_dpi) / screenDpi)
    widget: QWidget = QWidget()
    # physicalDpiY, logicalDpiY = widget.physicalDpiY(), widget.logicalDpiY()
    return int(points * widget.physicalDpiY() / widget.logicalDpiY())
    # return int(points * 96 / 72)


def pixelsToPoints(pixels):
    """
    Converts font size from pixels to points
    NOTE: We know that 1 inch = 96 pixels and 1 inch = 72 points
    Hence, 96 pixels = 72 points
    So, x pixels = x * 72 / 96 points"""
    # default_pix_per_inch = 96 if sys.platform == "win32" else 72
    # default_font_dpi = os.getenv("QT_FONT_DPI", default_pix_per_inch)
    # screenDpi = QGuiApplication.primaryScreen().physicalDotsPerInch()
    # return int((pixels / default_font_dpi) * screenDpi)
    return int(pixels * 72 / 96)


def get_logger(
    logger_name: str,
    level: int = logging.DEBUG,
    log_to_file: bool = False,
    file_logger_path: str = None,
) -> logging.Logger:
    """Return the logger with the name specified by logger_name arg.

    Args:
        logger_name (string): The name of logger (required!).
        level (int): logging level (optional, default = logging.DEBUG)
        log_to_file (bool): flag to indicate if logger should also log to file (other than console) (optional, default: True)
        file_logger_path (str): directory in which to create file logger [required if log_to_file is True, else ignored]

    Returns:
        Logger reformatted for this package.
    """
    logger = logging.getLogger(logger_name)
    logger.propagate = False
    logger.setLevel(level)

    formatter = logging.Formatter(
        "[%(name)s] [%(levelname)s] [%(asctime)s] %(message)s"
    )
    # create a console logger
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # create a file-handler (if asked for)
    if log_to_file:
        # create path of log file
        if file_logger_path is None:
            # create log in "logs" subfolder in dir from where this func was called
            calling_file_path = inspect.stack()[1].filename
            # Get the directory of the calling file (e.g., app.py)
            calling_dir = os.path.dirname(os.path.abspath(calling_file_path))
            logs_folder = os.path.join(calling_dir, "logs")
            if not os.path.exists(logs_folder):
                os.makedirs(logs_folder, exist_ok=True)
        now = datetime.now()
        log_file_name = f"{logger_name}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.log"
        log_file_path = os.path.join(logs_folder, log_file_name)

        # create file handler
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # logger.setLevel(level)
    # ch = logging.StreamHandler()
    # ch.setFormatter(formatter)
    # logger.addHandler(ch)
    return logger


# def get_logger(logger_name: str, level: int = logging.INFO) -> logging.Logger:
#     """Return the logger with the name specified by logger_name arg.

#     Args:
#         logger_name: The name of logger.

#     Returns:
#         Logger reformatted for this package.
#     """
#     logger = logging.getLogger(logger_name)
#     logger.propagate = False
#     logger.setLevel(level)
#     ch = logging.StreamHandler()
#     ch.setFormatter(
#         logging.Formatter("[%(name)s] [%(levelname)s] [%(asctime)s] %(message)s")
#     )
#     logger.addHandler(ch)
#     return logger


def centerOnScreenWithSize(
    widget: QWidget, widthProp: float, heightProp: float
) -> None:
    # center the widget on screen with size adjusted to widthProp & heightProp fraction of screem
    screenGeom: QRect = QGuiApplication.primaryScreen().geometry()
    widgetWidth: int = int(widthProp * screenGeom.width())
    widgetHeight: int = int(heightProp * screenGeom.height())
    widget.resize(QSize(widgetWidth, widgetHeight))

    x: int = int((screenGeom.width() - widget.width()) / 2)
    y: int = int((screenGeom.height() - widget.height()) / 2)
    widget.move(x, y)
