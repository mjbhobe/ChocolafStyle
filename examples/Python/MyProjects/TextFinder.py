# -*- coding: utf-8 -*-
# textFinder.py - based on Online example from Qt Documentation
import sys
import os
import pathlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from chocolaf.utils.chocolafapp import ChocolafApp

import TextFinderForm


class TextFinder(QWidget):
    def __init__(self):
        super(TextFinder, self).__init__()
        self.setWindowTitle(f'Text Finder Demo: PyQt {PYQT_VERSION_STR}')
        p = pathlib.Path(__file__)
        uiFilePath = os.path.join(os.path.split(str(p))[0], "TextFinder.ui")
        self.ui = uic.loadUi(uiFilePath, self)
        self.loadTextFile()
        # self.ui.textEdit.setEnabled(False)
        self.ui.textEdit.setReadOnly(True)
        self.ui.textEdit.setFont(QFont("Noto Mono, Source Code Pro, Consolas, SF Mono, Monospace", 10))
        self.ui.textEdit.setLineWrapMode(QTextEdit.WidgetWidth)
        # self.ui.findButton.setMinimumWidth(100)
        self.ui.findButton.clicked.connect(self.findButtonClicked)
        self.ui.openButton.clicked.connect(self.openButtonClicked)

    def loadTextFile(self, filePath: str = None):
        if filePath is None:
            p = pathlib.Path(__file__)
            filePath = os.path.join(os.path.split(str(p))[0], "input.txt")
        with open(filePath, 'r') as f:
            lines = ''.join(f.readlines())  # convert list to str
            # lines = ''.join(lines)
            self.ui.textEdit.setText(lines)

    def openButtonClicked(self):
        docsPath = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)
        filePath = QFileDialog.getOpenFileName(self, "Open File",
                                               docsPath[-1],
                                               "Text Files (*.txt *.c *.cpp *.h *.hxx *.py *.java *.bat *.sh)")
        if filePath:
            self.loadTextFile(filePath[0])

    def findButtonClicked(self):
        # move text cursor to beginning of text file
        cursor = self.ui.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor, 1)
        searchString = self.ui.findText.text()

        wholeWordsOnly = self.ui.wholeWordsCheck.isChecked()
        caseSensitive = self.ui.caseSensitiveCheck.isChecked()
        findFlags = QTextDocument.FindFlags(0)
        if caseSensitive and (not wholeWordsOnly):
            findFlags = QTextDocument.FindCaseSensitively
        elif (not caseSensitive) and wholeWordsOnly:
            findFlags = QTextDocument.FindWholeWords
        elif caseSensitive and wholeWordsOnly:
            findFlags = QTextDocument.FindCaseSensitively or QTextDocument.FindWholeWords

        if not (self.ui.textEdit.find(searchString, findFlags)):
            QMessageBox.information(self, "Search", f"No more occurances of <b>{searchString}</b>")


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
    # noinspection PyInterpreter
    with open(darkss_path, "r") as f:
        stylesheet = f.read()
    return stylesheet


def main():
    app = ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")

    w = TextFinder()
    w.setStyleSheet(app.getStyleSheet("Chocolaf"))
    w.show()
    w.move(100, 100)

    rect = w.geometry()
    w1 = TextFinder()
    w1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    w1.move(rect.left() + rect.width() + 50, rect.top() + rect.height() // 4 + 50)
    w1.show()

    return app.exec_()


if __name__ == "__main__":
    main()
