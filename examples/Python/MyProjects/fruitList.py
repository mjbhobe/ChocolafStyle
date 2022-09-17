"""
* fruitList.py - illustrates use of QListWidget & QDialog
* @author: Manish Bhobe
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import os
import pathlib
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp

FRUITS = ["Banana", "Apple", "Elderberry", "Clementine", "Fig",
          "Guava", "Mango", "Honeydew Melon", "Date", "Watermelon",
          "Tangerine", "Ugli Fruit", "Juniperberry", "Kiwi",
          "Lemon", "Nectarine", "Plum", "Raspberry", "Strawberry",
          "Orange"]


class Form(QWidget):
    def __init__(self, parent: QWidget = None):
        super(Form, self).__init__(parent)
        self.fruitsList = QListWidget()
        self.addBtn = QPushButton("&Add")
        self.editBtn = QPushButton("&Edit")
        self.removeBtn = QPushButton("&Remove")
        self.upBtn = QPushButton("&Up")
        self.downBtn = QPushButton("&Down")
        self.sortBtn = QPushButton("&Sort")
        self.closeBtn = QPushButton("&Close")
        self.setupUi()
        self.setWindowTitle("Fruits a-la-mondé")

    def setupUi(self):
        btnLayout = QVBoxLayout()
        btnLayout.addWidget(self.addBtn)
        btnLayout.addWidget(self.editBtn)
        btnLayout.addWidget(self.removeBtn)
        btnLayout.addWidget(self.upBtn)
        btnLayout.addWidget(self.downBtn)
        btnLayout.addWidget(self.sortBtn)
        btnLayout.addWidget(self.closeBtn)

        layout = QHBoxLayout()
        layout.addWidget(self.fruitsList)
        layout.addLayout(btnLayout)
        self.setLayout(layout)

        for fruit in FRUITS:
            listWidgetItem: QListWidgetItem = QListWidgetItem()
            listWidgetItem.setText(fruit)
            # self.fruitsList.addItem(fruit)
            self.fruitsList.addItem(listWidgetItem)

        self.closeBtn.clicked.connect(qApp.exit)

        self.setFocusProxy(self.fruitsList)


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
    # app.setStyle("Chocolaf")

    form = Form()
    form.move(100, 100)
    form.show()
    return app.exec()


if __name__ == "__main__":
    main()
