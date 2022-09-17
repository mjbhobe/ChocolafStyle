"""
* images.py - set image for label
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

app_dir = os.path.dirname(__file__)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.unchecked_text = "Check to see Mojo's picture"
        self.checked_text = "Uncheck to see Muffin's picture"
        self.mojo_image_path = os.path.join(app_dir, "images", "Mojo.jpg")
        self.muffin_image_path = os.path.join(
            app_dir, "images", "Muffin-2.jpg")
        self.setupUi()

    def setupUi(self):
        self.image_label = QLabel(f"")
        self.image_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        # pixmap = QPixmap(self.muffin_image_path)
        # self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(),
        #                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setScaledContents(True)
        self.checkbox = QCheckBox(self.unchecked_text)
        self.checkbox.clicked.connect(self.checkbox_clicked)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.checkbox)
        self.setLayout(layout)
        self.resize(980, 600)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} image labels")
        self.checkbox_clicked()

    def checkbox_clicked(self):
        if self.checkbox.isChecked():
            # show Mojo's picture
            image_path = self.mojo_image_path
            self.checkbox.setText(self.checked_text)
        else:
            # show Muffin's picture
            image_path = self.muffin_image_path
            self.checkbox.setText(self.unchecked_text)

        pixmap = QPixmap(image_path)
        # self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(),
        #                                          Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(),
                                                 Qt.KeepAspectRatio))
        self.setWindowTitle(
            f"PyQt {PYQT_VERSION_STR} image labels: {image_path}")


app = ChocolafApp(sys.argv)
# app.setStyle("QDarkStyle-dark")
app.setStyle("Chocolaf")
print('Hello World!')

win = Window()
win.show()

app.exec()
