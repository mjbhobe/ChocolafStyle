import os
import sys

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from chocolaf.utils.chocolafapp import ChocolafApp


class Form(QWidget):
    def __init__(self, title: str, parent: QWidget = None):
        super(Form, self).__init__(parent)

        layout = QVBoxLayout()

        glay = QGridLayout()

        self.label1 = QLabel("Normal QLabel")
        self.pgb1 = QProgressBar()
        self.pgb1.setRange(0, 100)
        self.pgb1.setValue(65)
        self.pgb2 = QProgressBar()
        self.pgb2.setRange(0, 100)
        self.pgb2.setValue(55)
        self.pgb2.setEnabled(False)
        glay.addWidget(self.label1, 0, 0)
        glay.addWidget(self.pgb1, 0, 1)
        glay.addWidget(self.pgb2, 0, 2)

        self.label2 = QLabel("Disabled QLabel")
        self.label2.setEnabled(False)
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider1.setRange(0, 100)
        self.slider1.setValue(65)
        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.setRange(0, 100)
        self.slider2.setValue(75)
        self.slider2.setEnabled(False)

        self.slider1.valueChanged.connect(self.slider1_valueChanged)

        glay.addWidget(self.label2, 1, 0)
        glay.addWidget(self.slider1, 1, 1)
        glay.addWidget(self.slider2, 1, 2)

        self.slider3 = QSlider(Qt.Vertical)
        self.slider3.setRange(0, 100)
        self.slider3.setValue(65)
        self.slider4 = QSlider(Qt.Vertical)
        self.slider4.setRange(0, 100)
        self.slider4.setValue(75)
        self.slider4.setEnabled(False)
        glay.addWidget(self.slider3, 0, 3, 2, 1)
        glay.addWidget(self.slider4, 0, 4, 2, 1)

        self.slider3.valueChanged.connect(self.slider3_valueChanged)

        self.label3 = QLabel("First name:")
        self.le1 = QLineEdit()
        self.label4 = QLabel("Last name:")
        self.le2 = QLineEdit()
        self.le2.setEnabled(False)
        self.pbg = QPushButton("Message")
        self.pbg.setEnabled(False)
        h1 = QHBoxLayout()
        h1.addWidget(self.label3)
        h1.addWidget(self.le1)
        h1.addWidget(self.label4)
        h1.addWidget(self.le2)
        h1.addWidget(self.pbg)
        self.le1.textChanged.connect(self.nameChanged)
        self.le2.textChanged.connect(self.nameChanged)
        self.pbg.clicked.connect(self.showMessage)
        glay.addLayout(h1, 2, 0, 1, 4)

        self.pb1 = QPushButton("Normal")
        self.pb2 = QPushButton("Disabled")
        self.pb2.setEnabled(False)
        self.pb3 = QPushButton("Checkable")
        self.pb3.setCheckable(True)
        self.pb4 = QPushButton("Chec-Disab")
        self.pb4.setCheckable(True)
        self.pb4.setChecked(True)
        self.pb4.setEnabled(False)
        self.pb5 = QPushButton("Default")
        self.pb5.setDefault(True)
        h2 = QHBoxLayout()
        h2.addWidget(self.pb1)
        h2.addWidget(self.pb2)
        h2.addWidget(self.pb3)
        h2.addWidget(self.pb4)
        h2.addWidget(self.pb5)
        # h1.addStretch()
        glay.addLayout(h2, 3, 0, 1, 4)

        self.pb5.clicked.connect(qApp.quit)

        layout.addLayout(glay)
        self.setLayout(layout)
        self.setToolTip("<b>This is widget tooltip</b><br/>You can use <i>rich</i> text too!")
        self.setWindowTitle(title)

    def slider1_valueChanged(self):
        self.pgb1.setValue(self.slider1.value())
        self.slider2.setValue(self.slider1.value())

    def slider3_valueChanged(self):
        self.pgb2.setValue(self.slider3.value())
        self.slider4.setValue(self.slider3.value())

    def nameChanged(self):
        enableLe2 = len(self.le1.text().strip()) != 0
        enableBtn: bool = (len(self.le1.text().strip()) != 0) and\
            (len(self.le2.text().strip()) != 0)
        self.le2.setEnabled(enableLe2)
        self.pbg.setEnabled(enableBtn)

    def showMessage(self):
        name: str = " ".join([self.le1.text().strip(), self.le2.text().strip()])
        QMessageBox.information(self, "Message",
                                f"Hello {name} - hope you are enjoying this theme")


def loadStyleSheet() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    print(f"loasStyleSteet() -> You are {here}")
    darkss_dir = os.path.join(here, "styles", "dark")
    sys.path.append(darkss_dir)
    import stylesheet_rc

    darkss_path = os.path.join(darkss_dir, "stylesheet.css")
    assert os.path.exists(darkss_path)
    print(f"LoasStyleSheet() -> loading dark stylesheet from {darkss_path}")
    stylesheet = ""
    with open(darkss_path, "r") as f:
        stylesheet = f.read()
    return stylesheet


def main():
    app = ChocolafApp(sys.argv)

    w = Form("Using my stylesheet")
    w.setStyleSheet(app.getStyleSheet("Chocolaf"))
    w.move(20, 20)
    w.show()

    rect = w.geometry()
    w1 = Form("Using QDarkStyle (Dark)")
    w1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    w1.move(rect.left() + rect.width() // 2, rect.top() + rect.height() + 50)
    w1.show()

    rect = w1.geometry()
    w2 = Form("Using QDarkStyle (Light)")
    w2.setStyleSheet(app.getStyleSheet("QDarkStyle-light"))
    w2.move(rect.left() + rect.width() // 2, rect.top() + rect.height() + 50)
    w2.show()

    return app.exec()


if __name__ == "__main__":
    main()
