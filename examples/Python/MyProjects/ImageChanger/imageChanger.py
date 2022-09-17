import sys
from PyQt5.QtGui import *
from mainWindow import *

from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp


def main():
    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    mainWindow = MainWindow()
    mainWindow.setWindowTitle(f"PyQt {PYQT_VERSION_STR} ImageChanger")
    mainWindow.resize(1024, 650)
    mainWindow.move(100, 100)
    mainWindow.show()

    return app.exec()


if __name__ == "__main__":
    main()
