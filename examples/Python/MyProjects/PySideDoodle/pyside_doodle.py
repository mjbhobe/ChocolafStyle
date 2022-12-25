import sys
from PySide6 import QtCore
from PySide6 import QtWidgets


def setupAppForHighDpiScreens():
    """ enables scaling for high DPI screens """
    if sys.platform == "win32":
        # Windows only
        # @see: https://vicrucann.github.io/tutorials/osg-qt-high-dpi/
        # @see: https://stackoverflow.com/questions/44398075/can-dpi-scaling-be-enabled-disabled-programmatically-on-a-per-session-basis
        import ctypes
        # 0 - unaware, 1 - system dpi aware, 2 - per monitor DPI aware
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DisableHighDpiScaling, True)
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    else:
        if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
            QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

            if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
                QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
