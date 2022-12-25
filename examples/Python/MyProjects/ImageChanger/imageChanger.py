import sys
from PyQt5.QtGui import *
from mainWindow import *

import chocolaf


def main():
    chocolaf.enable_hi_dpi()
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    mainWindow = MainWindow()
    mainWindow.setWindowTitle(f"PyQt {PYQT_VERSION_STR} ImageChanger")
    mainWindow.resize(1024, 650)
    mainWindow.move(100, 100)
    mainWindow.show()

    return app.exec()


if __name__ == "__main__":
    main()
