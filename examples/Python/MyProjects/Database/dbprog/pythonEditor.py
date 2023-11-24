import sys
import pathlib
from configparser import ConfigParser
import datetime

from PyQt6.QtCore import Qt, QLocale, QRegularExpression
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *

from syntaxeditor import TextEditor, PythonSyntaxHighlighter


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Python Syntax Editor")
        self.resize(800, 600)

        self.pythonEditor = TextEditor()
        self.highlighter = PythonSyntaxHighlighter(self.pythonEditor.document())

        self.setCentralWidget(self.pythonEditor)

        # open this file & show
        this_file_path = pathlib.Path(__file__)
        with open(str(this_file_path)) as f:
            text = f.read()
            self.pythonEditor.setText(text)

        self.setCentralWidget(self.pythonEditor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
