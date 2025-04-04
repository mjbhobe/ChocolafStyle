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

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

import chocolaf


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
            ("Push clostBtn", QPushButton),
            ("Radio clostBtn", QRadioButton),
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


chocolaf.enable_hi_dpi()
app = chocolaf.ChocolafApp(sys.argv)
# app.setStyle("Fusion")
app.setStyle("Chocolaf")

win = MainWindow()
win.show()

app.exec()
