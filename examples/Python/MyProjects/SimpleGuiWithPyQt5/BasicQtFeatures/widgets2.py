"""
* widgets2.py - label and checkbox
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


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.unchecked_text = "I am an unchecked checkbox, yet I can't roam free!"
        self.checked_text = "I am an checked checkbox, always in check"
        self.setupUi()

    def setupUi(self):
        self.label = QLabel(f"Click the checkbox & see it's text change")
        self.label.setAlignment(Qt.AlignCenter)
        self.checkbox = QCheckBox(self.unchecked_text)
        self.checkbox.clicked.connect(self.checkbox_clicked)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.checkbox)
        self.setLayout(layout)
        self.resize(640, 200)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} label & checkbox")

    def checkbox_clicked(self):
        checkbox_text = self.checked_text if self.checkbox.isChecked() else self.unchecked_text
        self.checkbox.setText(checkbox_text)


app = ChocolafApp(sys.argv)
# app.setStyle("QDarkStyle-dark")

win = Window()
win.show()

app.exec()
