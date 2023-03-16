# -*- coding: utf-8 -*-
"""
MIT License
===========
The spyder/images dir and some source files under other terms (see NOTICE.txt).
Copyright (c) 2009- Spyder Project Contributors and others (see AUTHORS.txt)
Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:
The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

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

version_info = (1, 0, 0, "dev0")

__version__ = '.'.join(map(str, version_info))
__installer_version__ = __version__
__title__ = "Chocolaf"
__author__ = "Manish Bhobé"
__organization__ = "Nämostuté Ltd."
__org_domain__ = "namostute.pyqtapps.in"
__license__ = __doc__
__project_url__ = "https://github.com/mjbhobe/ChocolafStyle"

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


# local imports
from .utilities import seed_all, enable_hi_dpi, pixelsToPoints, pointsToPixels, get_logger
from .app import ChocolafApp
from .palettes import ChocolafPalette, WinDarkPalette
from .styles.chocolaf import chocolaf_rc
from .icons import get_icon, get_icon_names
