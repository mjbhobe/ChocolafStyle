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
import logging
import os
import sys

__version__ = "1.0"
__author__ = "Manish Bhobé"
__organization__ = "Nämostuté Ltd."
__org_domain__ = "namostute.pyqtapps.in"

_logger = logging.getLogger(__name__)


def loadStyleSheet() -> str:
    """ loads the chocolaf stylesheet from ./styes/chocolaf """
    here = os.path.dirname(os.path.abspath(__file__))
    chocolaf_dir = os.path.join(here, "styles", "chocolaf")
    sys.path.append(chocolaf_dir)
    # this has all stylesheet specific images

    chocolaf_ss_path = os.path.join(chocolaf_dir, "chocolaf.css")
    assert os.path.exists(chocolaf_ss_path)
    _logger.info(f"Loaded chocolaf stylesheet from {chocolaf_ss_path}")
    stylesheet = ""
    with open(chocolaf_ss_path, "r") as f:
        stylesheet = f.read()
    return stylesheet


from chocolaf.utilities import seed_all, enable_hi_dpi, pixelsToPoints, pointsToPixels
from chocolaf.app import ChocolafApp
from chocolaf.palettes import ChocolafPalette
from chocolaf.styles.chocolaf import chocolaf_rc
