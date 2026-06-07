"""
horizontal_box.py - illustrated use of QHBoxLayout

@author: Manish Bhobe
My Experiments with Python and PyQt
Code shared for learning purposes only!
"""

import sys
from PyQt6.QtCore import PYQT_VERSION_STR
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUi()

    def initializeUi(self):
        """setup the GUI"""
        self.setMinimumWidth(500)
        self.setFixedHeight(60)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} - QHBoxLayout Demo")
        self.setupMainWindow()

    def setupMainWindow(self):
        """create the widgets, signals/slots in main window"""
        name_label = QLabel("New username:")
        name_edit = QLineEdit()
        name_edit.setClearButtonEnabled(True)
        # setup signal/slot for any edits to text
        name_edit.textEdited.connect(self.checkUserInput)

        self.accept_button = QPushButton("Confirm")
        self.accept_button.setEnabled(False)
        self.accept_button.clicked.connect(self.close)

        # setup the layout
        main_hbox = QHBoxLayout()
        main_hbox.addWidget(name_label)
        main_hbox.addWidget(name_edit)
        main_hbox.addWidget(self.accept_button)
        self.setLayout(main_hbox)

    def checkUserInput(self, text):
        """slot for name_edit.textEdited signal"""
        # check length & content entered into text box
        # text length > 0 and text must contain only alphanumeric content
        if (len(text) > 0) and all(t.isalpha() or t.isdigit() for t in text):
            self.accept_button.setEnabled(True)
        else:
            self.accept_button.setEnabled(False)


def main():
    app: QApplication = QApplication(sys.argv)

    # create the main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
