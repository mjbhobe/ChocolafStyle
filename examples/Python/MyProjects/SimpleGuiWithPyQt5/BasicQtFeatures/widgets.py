"""
* widgets.py - create an instance of all core widgets & show
* @author (Chocolaf): Manish Bhobe
*
* Examples from book "Create Simple Gui Applications with Python & Qt5 - Martin Fitzpatrick"
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!
"""

import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp


class MainWindow(QMainWindow):
    # class variable
    clickCounts: int = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi()

    def setupUi(self):
        layout = QGridLayout()
        label_n_widgets = [
            ("Check box", QCheckBox),
            ("Combo box", QComboBox),
            ("Date Edit", QDateEdit),
            ("Date/Time Edit", QDateTimeEdit),
            ("Dial", QDial),
            ("Double Spinbox", QDoubleSpinBox),
            ("Font ComboBox", QFontComboBox),
            ("LCD Number", QLCDNumber),
            ("Label", QLabel),
            ("Line edit", QLineEdit),
            ("Progress bar", QProgressBar),
            ("Push button", QPushButton),
            ("Radio button", QRadioButton),
            ("Slider", QSlider),
            ("Spin box", QSpinBox),
            ("Time Edit", QTimeEdit),
        ]
        for row, label_n_widget in enumerate(label_n_widgets):
            label, w = label_n_widget
            layout.addWidget(QLabel(label), row, 0)
            if label == "Slider":
                layout.addWidget(QSlider(Qt.Horizontal), row, 1)
            else:
                layout.addWidget(w(), row, 1)  # create & add widget

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.resize(640, 200)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} core widgets")


app = ChocolafApp(sys.argv)
# app.setStyle("QDarkStyle-dark")

win = MainWindow()
win.show()

app.exec()
