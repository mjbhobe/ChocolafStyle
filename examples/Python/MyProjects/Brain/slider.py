""" scrollbar.py: handling scrollbars """
import sys
import pathlib
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.scrollbar = None
        self.label = None
        self.icon_path = str(pathlib.Path(__file__).parent / "Qt-logo.png")
        self.setupUi()

    def setupUi(self):
        self.setMinimumSize(400, 100)
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setRange(0, 100)
        self.label = QLabel("Value: ")
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setWindowIcon(QIcon(self.icon_path))
        self.slider.valueChanged.connect(self.displayValue)
        self.slider.setValue(20)

    def displayValue(self):
        value = self.sender().value()
        self.label.setText(f"Value: {value:3d}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.setWindowTitle("PyQt Slider Demo")
    win.show()

    return app.exec()


if __name__ == "__main__":
    main()
