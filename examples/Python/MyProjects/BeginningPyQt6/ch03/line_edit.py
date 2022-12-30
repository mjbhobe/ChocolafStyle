""" line_edit.py - example of using a QLineEdit in PyQt6 """
import sys

from PyQt6.QtCore import PYQT_VERSION_STR, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR}: Line edit example")
        self.setMaximumSize(310, 130)
        self.setupMainWindow()

    def setupMainWindow(self):
        QLabel("Please enter your name below:", self).move(70, 10)
        name_label = QLabel("Name:", self)
        name_label.move(20, 50)

        # author name
        self.name_edit = QLineEdit(self)
        self.name_edit.resize(212, 22)
        self.name_edit.move(70, 50)
        self.name_edit.textChanged.connect(self.textChanged)

        clear_button = QPushButton("Clear", self)
        clear_button.move(120, 90)
        clear_button.clicked.connect(self.clearText)

        self.accept_button = QPushButton("OK", self)
        self.accept_button.move(210, 90)
        self.accept_button.setEnabled(False)  # disanbled by default
        self.accept_button.clicked.connect(self.acceptText)

    def clearText(self):
        self.name_edit.clear()

    def acceptText(self):
        print(f"Hello {self.name_edit.text()}, welcome to PyQt6")
        self.close()

    def textChanged(self):
        self.accept_button.setEnabled(len(self.name_edit.text()) != 0)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # create the main window
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
