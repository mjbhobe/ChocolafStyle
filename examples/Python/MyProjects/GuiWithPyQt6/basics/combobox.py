# -*- coding: utf-8 -*-
"""
* combobox.py - using QComboBox widget
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
import sys
import os
import pathlib
import random

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import qtawesome as qta

import chocolaf

APP_PATH = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} - Labels"
HOME_DIR = str(pathlib.Path.home())

SEED = 41
random.seed(SEED)

frameworks = {
    # for rankings - https://blog.paperspace.com/15-deep-learning-frameworks/
    # name : rank
    "Tensorflow": 1,
    "Pytorch": 2,
    "Sonnet": 3,
    "CNTK": 4,
    "Caffe2": 5,
    "MxNet": 6,
    "Glucon": 7,
    "Theano": 8,
    "Deeplearning4j": 9,
    "ONXX": 10,
    "Keras": 11,
    "Lightning": 12,
    "H2O": 13,
    "Kaldi": 14,
    "TensorflowJS": 15
}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(Window_Title)
        self.combo = QComboBox()
        self.label = QLabel(f"Select your favourite Deep Learning Framework")
        framework_names = list(frameworks.keys())
        random.shuffle(framework_names)
        self.combo.addItems(framework_names)
        self.label2 = QLabel("")
        self.label2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        close_icon = qta.icon("fa.close")
        self.button = QPushButton(close_icon, "Quit!")
        self.setupUi()

    def setupUi(self):
        win = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        layout.addWidget(self.label2)
        layout2 = QHBoxLayout()
        layout2.addStretch()
        layout2.addWidget(self.button)
        layout.addLayout(layout2)
        win.setLayout(layout)

        # setup signals & slots
        self.combo.currentIndexChanged.connect(self.framework_index_changed)
        self.button.clicked.connect(QApplication.instance().quit)

        self.setCentralWidget(win)

    def framework_index_changed(self, index):
        name = self.combo.itemText(index)
        text = f"<html>You chose <b>{name}</b> which is ranked <b>{frameworks[name]}</b></html>"
        self.label2.setText(text)


# app = QApplication(sys.argv)
app = chocolaf.ChocolafApp(sys.argv)
app.setStyle("WindowsDark")

# here is the window
win = MainWindow()
win.show()
sys.exit(app.exec())
