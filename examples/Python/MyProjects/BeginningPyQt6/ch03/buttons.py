""" buttons.py - example of using a QPushButton in PyQt6 """
import sys

from PyQt6.QtCore import PYQT_VERSION_STR, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(MainWindow, self).__init__(parent)
        self.initializeUi()

    def initializeUi(self):
        self.setGeometry(100, 100, 250, 150)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR}: Pushbutton example")
        self.setupMainWindow()

    def setupMainWindow(self):
        self.times_pressed = 0
        self.name_label = QLabel("Don't press the button", self)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.move(60, 30)

        self.button = QPushButton("Push Me", self)
        self.button.move(80, 70)
        self.button.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        self.times_pressed += 1

        if self.times_pressed == 1:
            self.name_label.setText("Why'd you press me?")
        if self.times_pressed == 2:
            self.name_label.setText("I'm warning you.")
            self.button.setText("Feelin' Lucky?")
            self.button.adjustSize()
            self.button.move(70, 70)
        if self.times_pressed == 3:
            print("The window has been closed.")
            self.close()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # create the main window
    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
