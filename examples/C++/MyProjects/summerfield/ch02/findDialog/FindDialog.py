# findDialog.py - standard find dialog
import sys
import os
# import PySide2
# from PySide2.QtCore import *
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# code to avoid "Unable to locate plugin..." message
try:
    pyside_ver = PySide2.__version__  # should throw NameError
    dirname = os.path.dirname(PySide2.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    print(f"PySide plugin path - {plugin_path}")
except NameError:
    print('Looks like you are using PyQt5')
    pass   # using PyQt5, so ignore


class FindDialog(QDialog):
    try:
        # if using PySide2
        findSignal = Signal(bool, str, Qt.CaseSensitivity, bool)
    except NameError:
        # if using PyQt5
        findSignal = pyqtSignal(bool, str, Qt.CaseSensitivity, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.label = QLabel("Find &what:")
        self.lineEdit = QLineEdit()
        self.label.setBuddy(self.lineEdit)
        self.lineEdit.setMinimumWidth(250)
        self.caseCheckBox = QCheckBox("Match &case")
        self.backwardCheckBox = QCheckBox("Search &backward")
        self.wholeWordsCheckBox = QCheckBox("W&hole words only")
        self.findButton = QPushButton("&Find")
        self.findButton.setDefault(True)
        self.findButton.setMinimumWidth(100)
        self.findButton.setEnabled(False)
        self.closeButton = QPushButton("C&lose")

        # setup signals & slots
        self.lineEdit.textChanged.connect(self.enableFindButton)
        self.findButton.clicked.connect(self.findClicked)
        self.closeButton.clicked.connect(self.close)

        # arrange the controls
        topLeft = QHBoxLayout()
        topLeft.addWidget(self.label)
        topLeft.addWidget(self.lineEdit)

        search1 = QHBoxLayout()
        search1.addWidget(self.caseCheckBox)
        search1.addWidget(self.wholeWordsCheckBox)

        checkLayout = QVBoxLayout()
        checkLayout.addLayout(search1)
        checkLayout.addWidget(self.backwardCheckBox)

        left = QVBoxLayout()
        left.addLayout(topLeft)
        left.addLayout(checkLayout)

        right = QVBoxLayout()
        right.addWidget(self.findButton)
        right.addWidget(self.closeButton)

        main = QHBoxLayout()
        main.addLayout(left)
        main.addLayout(right)
        self.setLayout(main)

        self.setWindowTitle("Find")
        self.setFixedHeight(self.sizeHint().height())

    def findClicked(self):
        text = self.lineEdit.text()
        cs = Qt.CaseSensitive if self.caseCheckBox.isChecked() else Qt.CaseInsensitive
        wwo = self.wholeWordsCheckBox.isChecked()
        backward = True if self.backwardCheckBox.isChecked() else False
        self.findSignal.emit(backward, text, cs, wwo)

    def enableFindButton(self, text):
        emptyText = (len(text.strip()) == 0)
        self.findButton.setEnabled(not emptyText)


class MainWin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.btn = QPushButton('Call Find Dialog')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)
        self.btn.clicked.connect(self.btnClicked)

    def btnClicked(self):
        findDialog = FindDialog()
        findDialog.setFont(QApplication.font("QMenu"))
        # connect signal emitted by dialog to local function
        findDialog.findSignal.connect(self.findSignalRaised)
        findDialog.exec()

    def findSignalRaised(self, backward: bool, text: str, cs: Qt.CaseSensitivity, wwo: bool):
        print(f"Searching {'BACKWARD' if backward else 'FORWARD'} - text: {text}" +
              f" - case sensitive: {'Yes' if cs == Qt.CaseSensitive else 'No'}" +
              f" - whole words only: {'Yes' if wwo else 'No'}")


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
