# gotoCellDialog.py - standard find dialog
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


class GoToCellDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        p = pathlib.Path(__file__)
        uiFilePath = os.path.join(
            os.path.split(str(p))[0], "gotocelldialog.ui")
        self.ui = uic.loadUi(uiFilePath, self)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Goto Cell")
        regExp = QRegExp("[A-Za-z][1-9][0-9]{0,2}")
        self.ui.lineEdit.setValidator(QRegExpValidator(regExp, self))
        self.ui.okButton.setMinimumWidth(100)
        self.ui.cancelButton.setMinimumWidth(100)

        # setup signals & Slots
        self.ui.okButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)
        self.ui.lineEdit.textChanged.connect(self.lineEditTextChanged)

    def lineEditTextChanged(self):
        self.ui.okButton.setEnabled(self.ui.lineEdit.hasAcceptableInput())


class MainWin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.btn = QPushButton('Call GoToCellDialog')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)
        self.btn.clicked.connect(self.btnClicked)

    def btnClicked(self):
        gotoCellDialog = GoToCellDialog(self)
        gotoCellDialog.setFont(QApplication.font("QMenu"))
        if gotoCellDialog.exec_():
            print(f"Will go to cell {gotoCellDialog.ui.lineEdit.text()}")


def main():
    app = QApplication(sys.argv)
    app.setFont(QApplication.font("QMenu"))
    app.setStyle("Fusion")

    mainWin = MainWin()
    mainWin.setFont(QApplication.font("QMenu"))
    mainWin.show()

    return app.exec_()


if __name__ == "__main__":
    main()
