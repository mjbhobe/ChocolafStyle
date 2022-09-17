# -*- coding: utf-8 -*-
"""
* __init__.py - Chocolaf stylesheet for Qt & PyQt applications (dark chocolate theme)
* @author: Manish Bhobe
*
* Inspired by QDarkstyle (@see: https://github.com/ColinDuquesnoy/QDarkStyleSheet)
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys
import os
import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

__version__ = "1.0"
__author__ = "Manish Bhobe"

_logger = logging.getLogger(__name__)

def loadStyleSheet() -> str:
    """ loads the chocolaf stylesheet from ./styes/chocolaf """
    here = os.path.dirname(os.path.abspath(__file__))
    chocolaf_dir = os.path.join(here, "styles", "chocolaf")
    sys.path.append(chocolaf_dir)
    # this has all stylesheet specific images
    import chocolaf_rc

    chocolaf_ss_path = os.path.join(chocolaf_dir, "chocolaf.css")
    assert os.path.exists(chocolaf_ss_path)
    _logger.info(f"Loaded chocolaf stylesheet from {chocolaf_ss_path}")
    stylesheet = ""
    with open(chocolaf_ss_path, "r") as f:
        stylesheet = f.read()
    return stylesheet
