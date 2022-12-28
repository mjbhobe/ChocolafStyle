""" checkboxes.py - create the basic PyQt6 application """
import sys

from PyQt6.QtCore import PYQT_VERSION_STR, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QCheckBox


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        self.setGeometry(200, 100, 250, 150)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} checkboxes")
        self.setupMainWindow()

    def setupMainWindow(self):
        header_label = QLabel("Which shifts can you work?"
                              "(Please check all that apply)", self)
        header_label.setWordWrap(True)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.move(10, 10)

        # Set up the checkboxes
        morning_cb = QCheckBox("Morning [8 AM-2 PM]", self)
        morning_cb.move(40, 60)
        morning_cb.toggled.connect(self.printSelected)
        morning_cb.toggle()  # Uncomment to start checked
        after_cb = QCheckBox("Afternoon [1 PM-8 PM]", self)
        after_cb.move(40, 80)
        after_cb.toggled.connect(self.printSelected)
        night_cb = QCheckBox("Night [7 PM-3 AM]", self)
        night_cb.move(40, 100)
        night_cb.toggled.connect(self.printSelected)

    def printSelected(self, checked):
        """ print the text that teh sender is sending"""
        sender = self.sender()
        if (checked):
            print(f"{sender.text()} selected")
        else:
            print(f"{sender.text()} de-selected")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # create the main window
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
