# -*- coding: utf-8 -*-
"""
* labels2.py - display images on labels
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
import sys
import os
import pathlib
from PIL import Image
from PIL.ImageQt import ImageQt

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import chocolaf

APP_PATH = os.path.dirname(__file__)
HOME_DIR = str(pathlib.Path.home())
IMAGE_PATH = pathlib.Path(APP_PATH) / "images" / "Muffin.jpg"
Window_Title = f"PyQt {PYQT_VERSION_STR} QPixmap: {IMAGE_PATH.name}"


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(Window_Title)
        image = Image.open(str(IMAGE_PATH))
        image = image.resize((512, 256))
        # for some reason, image is being displayed upside down
        image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        qim = ImageQt(image)
        pixmap = QPixmap.fromImage(qim)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)


# app = QApplication(sys.argv)
app = chocolaf.ChocolafApp(sys.argv)
app.setStyle("WindowsDark")

# here is the window
win = MainWindow()
win.show()
sys.exit(app.exec())
