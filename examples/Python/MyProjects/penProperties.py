"""
* penProperties.py - illustrates a 'dumb' pen properties dialog
* @author: Manish Bhobe
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import os
import pathlib
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from chocolaf.utils.chocolafapp import ChocolafApp


class PenPropertiesDlg(QDialog):
    def __init__(self, parent: QWidget = None):
        super(PenPropertiesDlg, self).__init__(parent)
        self.widthLabel = QLabel("&Width:")
        self.widthSpinBox = QSpinBox()
        self.widthLabel.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.widthSpinBox.setRange(0, 24)
        self.beveledCheckBox = QCheckBox("&Beveled edges")
        self.styleLabel = QLabel("&Style:")
        self.styleComboBox = QComboBox()
        self.styleLabel.setBuddy(self.styleComboBox)
        self.styleComboBox.addItems(["Solid", "Dashed", "Dotted",
                                     "DashDotted", "DashDotDotted"])
        # self.okButton = QPushButton("&OK")
        # self.cancelButton = QPushButton("Cancel")
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        self.setupUi()
        self.setWindowTitle("Pen Properties")

    def setupUi(self):
        # buttonLayout = QHBoxLayout()
        # buttonLayout.addStretch()
        # buttonLayout.addWidget(self.okButton)
        # buttonLayout.addWidget(self.cancelButton)
        layout = QGridLayout()
        layout.addWidget(self.widthLabel, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(self.beveledCheckBox, 0, 2)
        layout.addWidget(self.styleLabel, 1, 0)
        layout.addWidget(self.styleComboBox, 1, 1, 1, 2)
        #layout.addLayout(buttonLayout, 2, 0, 1, 3)
        layout.addWidget(self.buttonBox, 3, 0, 1, 3)

        self.setLayout(layout)

        # self.okButton.clicked.connect(self.accept)
        # self.cancelButton.clicked.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


def loadStyleSheet() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    print(f"loasStyleSteet() -> You are {here}")
    darkss_dir = os.path.join(here, "styles", "dark")
    sys.path.append(darkss_dir)
    import stylesheet_rc

    darkss_path = os.path.join(darkss_dir, "stylesheet.css")
    assert os.path.exists(darkss_path)
    print(f"LoasStyleSheet() -> loading dark stylesheet from {darkss_path}")
    stylesheet = ""
    with open(darkss_path, "r") as f:
        stylesheet = f.read()
    return stylesheet


def main():
    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    dialog = PenPropertiesDlg(None)
    dialog.widthSpinBox.setValue(2)
    dialog.beveledCheckBox.setChecked(True)
    dialog.styleComboBox.setCurrentIndex(4)
    if dialog.exec() == QDialog.Accepted:
        print(f"Pen properties -> width: {dialog.widthSpinBox.value()} - " +
              f"beveled? : {'Yes' if dialog.beveledCheckBox.isChecked() else 'No'} - " +
              f"style: {dialog.styleComboBox.currentText()}")
    else:
        print("You CANCELLED the dialog")

    return 0


if __name__ == "__main__":
    main()
