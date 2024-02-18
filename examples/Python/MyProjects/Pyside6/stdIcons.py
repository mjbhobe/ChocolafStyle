# stdIcons - using standard icons available with PySide6
import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Window(QWidget):
    def __init__(self, parent: QWidget = None):
        super(Window, self).__init__(parent)
        # all standard icon names are available in QStyle and start with "SP_"
        icons = sorted(
            [attr for attr in dir(QStyle.StandardPixmap) if attr.startswith("SP_")]
        )
        layout = QGridLayout()

        for n, name in enumerate(icons):
            btn = QPushButton(name)

            pix = getattr(QStyle.StandardPixmap, name)
            icon = self.style().standardIcon(pix)
            btn.setIcon(icon)
            # add in a 6 x 6 grid
            layout.addWidget(btn, n // 6, n % 6)
        self.setLayout(layout)
        # self.setWindowTitle(f"PySide {qVersion()} - Standard Icons")
        self.setWindowTitle(f"PyQt6 {PYQT_VERSION_STR} - Standard Icons")
        self.setWindowIcon(
            self.style().standardIcon(
                getattr(QStyle.StandardPixmap, "SP_TitleBarMenuButton")
            )
        )


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # create & show GUI
    win = Window()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
