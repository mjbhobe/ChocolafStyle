"""
pythonEditor.py: simple syntax highlighting Python text editor that implements
    auto-indentation, smart-indentation
@author: Manish Bhobé
My Experiments with Python, Machine Learning, and Deep Learning
Code is distributed as-is for learning purposed only. Please use at your own risk.
"""

import sys
import pathlib

from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import *

from syntaxeditor import PythonTextEditor, PythonSyntaxHighlighter


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Python Syntax Editor")
        self.resize(800, 600)

        self.pythonEditor = PythonTextEditor()
        self.highlighter = PythonSyntaxHighlighter(self.pythonEditor.document())

        self.setCentralWidget(self.pythonEditor)

        # open this file & show
        this_file_path = pathlib.Path(__file__)
        this_file_path = "/tmp/scratch.py"
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
