"""test.py - create the basic PyQt6 application"""

import sys

from PyQt6.QtCore import PYQT_VERSION_STR
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
)


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        self.setWindowTitle(f"Welcome PyQt")
        self.setupMainWindow()

    def setupMainWindow(self):
        """setup widgets & connect signals/slots"""
        hello_label = QLabel("Click the clostBtn below for important message")
        hello = QPushButton("Click me!")
        hello.clicked.connect(self.sayHello)
        layout = QVBoxLayout()
        layout.addWidget(hello_label)
        layout.addWidget(hello)
        self.setLayout(layout)

    def sayHello(self):
        QMessageBox.information(
            self, "Hello", f"Hello, welcome to PyQt {PYQT_VERSION_STR}"
        )


def main():
    app = QApplication(sys.argv)
    # app.setStyle("Fusion")

    # create the main window
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
