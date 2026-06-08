"""
vertical_box.py - illustrated use of QVBoxLayout

@author: Manish Bhobe
My Experiments with Python and PyQt
Code shared for learning purposes only!
"""

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtCore import PYQT_VERSION_STR
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QButtonGroup,
    QCheckBox,
)
from PyQt6.QtGui import QFont

from chocolaf.utilities import create_base_font


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUi()

    def initializeUi(self):
        """setup the GUI"""
        self.setMinimumSize(350, 200)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} - QVBoxLayout Demo")
        self.base_font = create_base_font()
        self.setupMainWindow()

    def setupMainWindow(self):
        """create the widgets, signals/slots in main window"""
        header_label = QLabel(f"Feedback Form")
        header_label_font = QFont(self.base_font)
        header_label_font.setPointSize(18)
        header_label.setFont(header_label_font)
        header_label.setStyleSheet("color: rgb(0, 136, 255);")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        question_label = QLabel("How would you rate your service?")
        question_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        ratings = ["Excellent", "Good", "Average", "Poor"]
        ratings_group = QButtonGroup(self)
        ratings_group.buttonClicked.connect(self.checkbox_clicked)
        for i, rating in enumerate(ratings):
            checkbox = QCheckBox(rating, self)
            ratings_group.addButton(checkbox)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setEnabled(False)
        self.confirm_button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(header_label)
        layout.addWidget(question_label)
        print(f"There are {len(ratings_group.buttons())} checkboxes in the group")
        for checkbox in ratings_group.buttons():
            layout.addWidget(checkbox)
        layout.addWidget(self.confirm_button)
        self.setLayout(layout)

    def checkbox_clicked(self, button):
        """enable confirm button when any checkbox is selected"""
        print(f"Clicked checkbox: {button.text()}")
        self.confirm_button.setEnabled(True)


def main():
    app: QApplication = QApplication(sys.argv)

    # create the main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
