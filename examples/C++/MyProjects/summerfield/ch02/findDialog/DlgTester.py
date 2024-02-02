# DlgTester.py
import sys
import os
import pathlib
# import PySide2
# from PySide2.QtCore import *
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
# from PySide2.QtUiTools import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
# using qdarkstyle (@see: https://github.com/ColinDuquesnoy/QDarkStyleSheet)
import qdarkstyle
# to detect dark themes (@see: https://pypi.org/project/darkdetect/)
import darkdetect

from FindDialog import *
from GotoCellDialog import *

# code to avoid "Unable to locate plugin..." message
try:
    pyside_ver = PySide2.__version__  # should throw NameError
    dirname = os.path.dirname(PySide2.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    print(f"PySide plugin path - {plugin_path}")
    uiLoader = QUiLoader()
except NameError:
    print('Looks like you are using PyQt5')
    pass   # using PyQt5, so ignore


class DlgTester(QWidget):
    """ class to call FindDialog & GotoCellDialog """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Dialogs Tester")
        self.callFindDialogBtn = QPushButton('Call FindDialog')
        self.callFindDialogBtn.setMinimumWidth(300)
        self.callGotoCellDialogBtn = QPushButton('Call GotoCellDialog')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.callFindDialogBtn)
        self.layout.addWidget(self.callGotoCellDialogBtn)
        self.setLayout(self.layout)

        # setup signals & Slots
        self.callFindDialogBtn.clicked.connect(self.FindDlgButtonClicked)
        self.callGotoCellDialogBtn.clicked.connect(
            self.GotoCellDialogButtonClicked)

    def FindDlgButtonClicked(self):
        findDialog = FindDialog(self)
        findDialog.setFont(QApplication.font("QMenu"))
        # connect signal emitted by dialog to local function
        findDialog.findSignal.connect(self.findSignalRaised)
        findDialog.exec()

    def findSignalRaised(self, backward: bool, text: str, cs: Qt.CaseSensitivity, wwo: bool):
        print(f"Searching {'BACKWARD' if backward else 'FORWARD'} - text: {text}" +
              f" - case sensitive: {'Yes' if cs == Qt.CaseSensitive else 'No'}" +
              f" - whole words only: {'Yes' if wwo else 'No'}")

    def GotoCellDialogButtonClicked(self):
        gotoCellDialog = GoToCellDialog(self)
        gotoCellDialog.setFont(QApplication.font("QMenu"))
        if gotoCellDialog.exec():
            print(f"Will go to cell {gotoCellDialog.ui.lineEdit.text()}")


def main():
    app = QApplication(sys.argv)
    app.setFont(QApplication.font("QMenu"))
    app.setStyle("Fusion")
    if darkdetect.isDark():
        # apply dark stylesheet
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    dlgTester = DlgTester()
    dlgTester.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
