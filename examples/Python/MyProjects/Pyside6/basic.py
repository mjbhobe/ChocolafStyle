# basic.py - hello world with PySide6
import sys
from PySide6.QtWidgets import QApplication, QWidget


def main():
    # Step1: create an instance of QApplication
    app: QApplication = QApplication(sys.argv)

    # create the gui
    win: QWidget = QWidget()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
