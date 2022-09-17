"""
* MyApp.py - simple Qt Application
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
        self.labelText = f"This is a PyQt {PYQT_VERSION_STR} application"
        self.label = QLabel(self.labelText)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(22, 22))
        self.addToolBar(self.toolbar)

        # create actions
        appDir = os.path.dirname(__file__)
        click_image_path = os.path.join(appDir, "images", "click.png")
        assert(os.path.exists(click_image_path))
        toggle_image_path = os.path.join(appDir, "images", "toggle.png")
        assert(os.path.exists(toggle_image_path))
        exit_image_path = os.path.join(appDir, "images", "exit.png")
        assert(os.path.exists(exit_image_path))

        self.button1_action = QAction(
            QIcon(click_image_path), "Click Button", self)
        self.button1_action.setStatusTip("Click count button")
        # add shortcut (Ctrl+K)
        self.button1_action.setShortcut("Ctrl+k")
        self.button1_action.triggered.connect(self.button1Clicked)

        self.button2_action = QAction(
            QIcon(toggle_image_path), "Toggle Button", self)
        self.button2_action.setStatusTip("Toggle Button")
        self.button2_action.setCheckable(True)
        # add shortcut (Ctrl+T)
        self.button2_action.setShortcut(Qt.CTRL + Qt.Key_T)
        self.button2_action.triggered.connect(self.button2Clicked)
        self.exitAction = QAction(
            QIcon(exit_image_path), "Exit Application", self)
        self.exitAction.triggered.connect(qApp.exit)

        self.toolbar.addAction(self.button1_action)
        self.toolbar.addAction(self.button2_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.exitAction)

        # create a menubar & add same actions
        menu = self.menuBar()
        actMenu = menu.addMenu("&Actions")
        actMenu.addAction(self.button1_action)
        actMenu.addAction(self.button2_action)
        actMenu.addSeparator()
        actMenu.addAction(self.exitAction)

        self.statusBar().showMessage("")

        self.resize(640, 200)
        self.setWindowTitle("My first PyQt App")

    def button1Clicked(self):
        MainWindow.clickCounts += 1
        txt = f"{self.labelText} - click count = {MainWindow.clickCounts:4d}"
        self.label.setText(txt)

    def button2Clicked(self):
        txt = f"{self.labelText} - button is {'ON' if self.button2_action.isChecked() else 'OFF'}"
        self.label.setText(txt)


app = ChocolafApp(sys.argv)
# app.setStyle("Fusion")

win = MainWindow()
win.show()

app.exec()
