import os
import random
import logging
import pathlib
from datetime import datetime
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme

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
    np.random.seed(seed)
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
    file_path: pathlib.Path, level: int = logging.INFO, custom_theme: Theme = None
) -> logging.Logger:
    """
    gets a standard logger with 2 handlers - a stream handler (console) and a file handler.
    The stream handler respects the level passed in as a parameter, whereas the file-handler
    always sets logging level to logging.DEBUG (to log all messages to file).
    Both handlers use the same formatter, which logs with following format:
        "[%(name)s] [%(levelname)s] [%(asctime)s] %(message)s"

    @params:
        file_path (required, pathlib.Path): usually full path of program from where this function is called
            (file logging creates a log file in the logs subfolder of this path)
        level (optional, int - default = logging.INFO) - the logging level of the stream (console) logger
            (level of file logger is always set to logging.DEBUG)
        custom_theme (optional, Theme - default = None) - custom theme for the logger (applied to console handler only!)

    @returns:
        logging.Logger - the logger objects, which should be passed to the Trainer object to log progress
    """

    assert (
        file_path.is_file()
    ), f"FATAL ERROR: get_logger() -> file_path parameter must be a valid path to existing file!"
    name = file_path.stem
    # replace extension of file_path with .log
    # log_path = file_path.with_suffix(".log")
    log_dir = file_path.parent / "logs"
    # log_dir does not exist, create it
    log_dir.mkdir(exist_ok=True)
    now = datetime.now()
    now_str = datetime.strftime(now, "%Y%m%d-%H%M%S")
    log_path = f"{log_dir}/{name}_{now_str}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # common formatter
    formatter = logging.Formatter(
        "[%(name)s] [%(levelname)s] [%(asctime)s] %(message)s",
        datefmt="%Y-%b-%d %H:%M:%S",
    )

    # create handlers
    # stream_handler = logging.StreamHandler()
    # replace stream handler with console handler for colorful logging to console
    if custom_theme is None:
        custom_theme = Theme({
            "logging.level.debug": "green",
            "logging.level.info": "sky_blue1",
            "logging.level.warning": "orange3",
            "logging.level.error": "red",
            "logging.level.critical": "bright_red",
        })
    custom_console = Console(theme=custom_theme)
    stream_handler = RichHandler(
        console=custom_console, 
        markup=True,
        show_level=True,
        show_time=True, 
        show_path=True,
    )
    stream_handler.setLevel(level)
    # stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    # Avoid duplicate logs by ensuring handlers are not added multiple times
    logger.propagate = False

    return logger


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
