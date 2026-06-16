"""
grid_layout.py - laying out widgets in a Grid

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
        self.setMinimumSize(600, 160)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} - Nested Layouts")
        self.base_font = create_base_font()
        self.setupMainWindow()

    def setupMainWindow(self):
        """create the widgets, signals/slots in main window"""

        # widgets on left side of window
        header_label = QLabel("Simple Daily Planner")
        header_label_font = QFont(self.base_font)
        header_label_font.setPointSize(18)
        header_label.setFont(header_label_font)

        today_label = QLabel("* Today's focus")
        today_label_font = QFont(self.base_font)
        today_label_font.setPointSize(12)
        today_label.setFont(today_label_font)
        self.today_edit = QTextEdit()

        notes_label = QLabel("* Notes")
        notes_label_font = QFont(self.base_font)
        notes_label_font.setPointSize(12)
        notes_label.setFont(notes_label_font)

        self.notes_edit = QTextEdit()

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(header_label, 0, 0)
        self.main_layout.addWidget(today_label, 1, 0)
        self.main_layout.addWidget(self.today_edit, 2, 0, 3, 1)
        self.main_layout.addWidget(notes_label, 5, 0)
        self.main_layout.addWidget(self.notes_edit, 6, 0, 3, 1)

        # create widgets for right side
        today = QDate.currentDate().toString(Qt.DateFormat.ISODate)
        date_label = QLabel(today)
        date_label_font = QFont(self.base_font)
        date_label_font.setPointSize(14)
        date_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        date_label.setFont(date_label_font)

        todo_label = QLabel("* To Do")
        todo_label_font = QFont(self.base_font)
        todo_label_font.setPointSize(12)
        todo_label.setFont(todo_label_font)

        self.main_layout.addWidget(date_label, 0, 2)
        self.main_layout.addWidget(todo_label, 1, 1, 1, 2)

        for row in range(2, 9):
            item_cb = QCheckBox()
            item_edit = QLineEdit()
            self.main_layout.addWidget(item_cb, row, 1)
            self.main_layout.addWidget(item_edit, row, 2)

        self.setLayout(self.main_layout)


def main():
    app: QApplication = QApplication(sys.argv)

    # create the main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
