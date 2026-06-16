"""
nested_layout.py - PyQt6 Nested Layout Example

Sometimes, a single layout manager won't be able to suit all of your needs as your
interfaces become more complex. Fortunately, handling this matter isn't too difficult
with PyQt as you can arrange layouts inside of other layouts to solve intricate
arrangement issues.

@author: Manish Bhobe
My Experiments with Python and PyQt
Code shared for learning purposes only!
"""

import sys
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtCore import PYQT_VERSION_STR
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QCheckBox,
    QTextEdit,
    QGridLayout,
)
from PyQt6.QtGui import QFont

from chocolaf.utilities import create_base_font


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUi()

    def initializeUi(self):
        """setup the GUI"""
        self.setMinimumSize(400, 160)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} - Nested Layouts")
        self.base_font = create_base_font()
        self.setupMainWindow()

    def setupMainWindow(self):
        """create the widgets, signals/slots in main window"""
        info_label = QLabel("Select 2 items for lunch & their prices")
        info_label_font = QFont(self.base_font)
        info_label_font.setPointSize(16)
        info_label.setFont(info_label_font)
        info_label.setStyleSheet("color: rgb(0, 136, 255);")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # create the list of food items, which will be displayed in 2 combo-boxes
        # Create a list of food items and two separate
        # QComboBox widgets to display all of the items
        # fmt: off
        food_list = [
            "egg", "turkey sandwich", "ham sandwich", "cheese", "hummus",
            "yogurt", "apple", "banana", "orange", "waffle", "carrots",
            "bread", "pasta", "crackers", "pretzels", "coffee", "soda", "water"
        ]
        # fmt: on
        food_combo1 = QComboBox()
        food_combo1.addItems(food_list)
        food_combo2 = QComboBox()
        food_combo2.addItems(food_list)

        # Create two QSpinBox widgets to display prices
        self.price_sb1 = QSpinBox()
        self.price_sb1.setRange(0, 100)
        self.price_sb1.setPrefix("$")
        self.price_sb1.valueChanged.connect(self.calculateTotal)
        self.price_sb2 = QSpinBox()
        self.price_sb2.setRange(0, 100)
        self.price_sb2.setPrefix("$")
        self.price_sb2.valueChanged.connect(self.calculateTotal)

        # arrange your widgets in nested layouts
        hbox_1 = QHBoxLayout()
        hbox_1.addWidget(food_combo1)
        hbox_1.addWidget(self.price_sb1)

        hbox_2 = QHBoxLayout()
        hbox_2.addWidget(food_combo2)
        hbox_2.addWidget(self.price_sb2)

        self.total_label = QLabel("Total Spent: $")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        total_label_font = QFont(self.base_font)
        total_label_font.setPointSize(12)
        self.total_label.setFont(total_label_font)
        self.total_label.setStyleSheet("color: rgb(0, 136, 255);")

        main_vbox = QVBoxLayout()
        main_vbox.addWidget(info_label)
        main_vbox.addLayout(hbox_1)
        main_vbox.addLayout(hbox_2)
        main_vbox.addWidget(self.total_label)

        self.setLayout(main_vbox)

    def calculateTotal(self):
        total = self.price_sb1.value() + self.price_sb2.value()
        self.total_label.setText(f"Total Spent: $ {total}")


def main():
    app: QApplication = QApplication(sys.argv)

    # create the main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
