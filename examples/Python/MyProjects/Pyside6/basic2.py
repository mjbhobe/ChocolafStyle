# basic.py - hello world with PySide6
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QSlider,
)


def slider_changed(data):
    print(f"Slider moved to {data}!")


def main():
    # Step1: create an instance of QApplication
    app: QApplication = QApplication(sys.argv)

    # create the gui
    slider = QSlider(Qt.Horizontal)
    slider.setRange(0, 100)
    slider.valueChanged.connect(slider_changed)
    slider.setValue(25)
    slider.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
