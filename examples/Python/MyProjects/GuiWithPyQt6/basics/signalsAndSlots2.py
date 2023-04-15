# -*- coding: utf-8 -*-
"""
* signalsAndSlots2.py - update other GUI components on click of button
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!

"""
import sys
import os
import pathlib

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import chocolaf
import qtawesome as qta  # SVG icons

APP_PATH = os.path.dirname(__file__)
Window_Title = f"PyQt {PYQT_VERSION_STR} - Signals & Slots-2"
HOME_DIR = str(pathlib.Path.home())

MESSAGES = [
    "You clicked me once",
    "You clicked me again",
    "You clicked me once again",
    "Hey, what's up with the clicking man?",
    "Stop it! This is getting on my nerves",
    "Last warning - one more & we are done",
    "You did not listen. Now you die!"
]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.icon = qta.icon("fa.check")
        self.button = QPushButton(self.icon, "Click Me")
        self.label = QLabel("Click the button to see a new message")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.index = 0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle(Window_Title)
        win = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        win.setLayout(layout)
        self.setCentralWidget(win)
        self.setFixedSize(QSize(300, 100))
        # setup signals & slots
        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        if self.index < len(MESSAGES) - 1:
            self.label.setText(MESSAGES[self.index])
            self.index += 1
        else:
            msgBox: QMessageBox = QMessageBox()
            msgBox.setText(MESSAGES[-1])
            msgBox.setWindowTitle("That was your last warning!")
            msgBox.setInformativeText("The application will close now because you didn't listen")
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.exec()
            QApplication.instance().quit()


# app = QApplication(sys.argv)
app = chocolaf.ChocolafApp(sys.argv)
app.setStyle("WindowsDark")
# app.setStyle("Fusion")

# here is the window
win = MainWindow()
win.show()
sys.exit(app.exec())
