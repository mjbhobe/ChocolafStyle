#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* scrollArea.py - displays an image, specified on command line, in QScrollArea
* @author: Manish Bhobe
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys
import os
import pathlib
from argparse import ArgumentParser
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import darkdetect

sys.path.append(os.path.join(pathlib.Path(__file__).parents[3], 'common_files'))
from mypyqt5_utils import PyQtApp

class ScrollWindow(QMainWindow):
    def __init__(self, imagePath : str, parent : QWidget = None):
        super(ScrollWindow, self).__init__(parent)
        assert os.path.exists(imagePath), f"{imagePath} - image does not exist!"
        self.label = QLabel("")
        image = QImage()
        image.load(imagePath)
        self.label.setPixmap(QPixmap.fromImage(image))
        # add our scroll area here
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.label)
        self.scrollArea.viewport().setBackgroundRole(QPalette.Dark)
        self.scrollArea.viewport().setAutoFillBackground(True)
        self.setCentralWidget(self.scrollArea)
        self.setWindowTitle(f"QScrollArea demo: {imagePath}")
        self.resize(640, 480)

def main():
    ap = ArgumentParser()
    ap.add_argument("-i", "--image", required = True,
                    help = "Full path to image")
    args = vars(ap.parse_args())

    if os.path.exists(args["image"]):
        app = PyQtApp(sys.argv)

        win = ScrollWindow(args['image'])
        win.setFont(app.getFont())
        win.show()

        return app.exec()
    else:
        print(f"FATAL: {args['image']} - path does not exist!")


if __name__ == "__main__":
    main()
