#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* splitters.py - verticle split into 3 using splitters
* @author (Chocolaf): Manish Bhobe
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp


def createGui():
    text1 = \
        """Mon enfant, ma sœur, pense à la douceur d'y aller vivre ensemble ; Aimer à loisir, aimer et mourir, dans un pays qui est à votre image!
        """
    text2 = \
        """My child, my sister, think of the sweetness of going there to live together; To love at leisure, to love and to die, in a country that is an image of you!
        """
    text3 = \
        """मेरे बच्चे, मेरी बहन, एक साथ रहने के लिए वहाँ जाने की मिठास के बारे में सोचो; फुर्सत में प्यार करना, प्यार करना और मरना, एक ऐसे देश में जो आपकी एक छवि है!
        """
    editor1 = QTextEdit()
    editor1.setText(text1)
    editor2 = QTextEdit()
    editor2.setText(text2)
    editor3 = QTextEdit()
    editor3.setText(text3)

    splitter = QSplitter(Qt.Horizontal)
    splitter.addWidget(editor1)
    splitter.addWidget(editor2)
    splitter.addWidget(editor3)
    return splitter


def main():
    # app = ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")
    app = QApplication(sys.argv)

    # create & show GUI
    splitter = createGui()
    splitter.setWindowTitle("Horizontal QSplitter Demo")
    splitter.show()

    return app.exec()


if __name__ == "__main__":
    main()
