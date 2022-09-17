"""
* lineEdits.py - various types of single line edit widgets using Chocolaf
* @author (Chocolaf): Manish Bhobe
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""

#############################################################################
##
# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
##
# This file is part of the examples of PyQt.
##
# $QT_BEGIN_LICENSE:BSD$
# You may use this file under the terms of the BSD license as follows:
##
# "Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the
# distribution.
# * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
# the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
##
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
# $QT_END_LICENSE$
##
#############################################################################


import os
import pathlib
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp


class Window(QWidget):
    def __init__(self, parent: QWidget = None):
        super(Window, self).__init__(parent)
        self.echoGroup = self.createEchoGroup()
        self.validatorGroup = self.createValidatorGroup()
        self.alignmentGroup = self.createAlignmentGroup()
        self.inputMaskGroup = self.createInputMaskGroup()
        self.accessGroup = self.createAccessGroup()

        layout = QGridLayout()
        layout.addWidget(self.echoGroup, 0, 0)
        layout.addWidget(self.inputMaskGroup, 0, 1)
        layout.addWidget(self.validatorGroup, 1, 0)
        layout.addWidget(self.accessGroup, 1, 1)
        layout.addWidget(self.alignmentGroup, 2, 0)
        self.setLayout(layout)
        self.setWindowTitle("Line Edits")

    def createEchoGroup(self) -> QGroupBox:
        echoGroup = QGroupBox("Echo")

        echoLabel = QLabel("Mode:")
        echoComboBox = QComboBox()
        echoComboBox.addItem("Normal")
        echoComboBox.addItem("Password")
        echoComboBox.addItem("PasswordEchoOnEdit")
        echoComboBox.addItem("No Echo")
        # echoComboBox.setEditable(True)

        self.echoLineEdit = QLineEdit()
        self.echoLineEdit.setPlaceholderText("Placeholder Text")
        self.echoLineEdit.setFocus()

        # signal & slot
        echoComboBox.activated.connect(self.echoChanged)

        # layout
        echoLayout = QGridLayout()
        echoLayout.addWidget(echoLabel, 0, 0)
        echoLayout.addWidget(echoComboBox, 0, 1)
        echoLayout.addWidget(self.echoLineEdit, 1, 0, 1, 2)
        echoGroup.setLayout(echoLayout)
        return echoGroup

    def echoChanged(self, index: int):
        if index == 0:
            self.echoLineEdit.setEchoMode(QLineEdit.Normal)
        elif index == 1:
            self.echoLineEdit.setEchoMode(QLineEdit.Password)
        elif index == 2:
            self.echoLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        elif index == 3:
            self.echoLineEdit.setEchoMode(QLineEdit.NoEcho)

    def createValidatorGroup(self) -> QGroupBox:
        validatorGroup = QGroupBox("Validator")

        validatorLabel = QLabel("Type:")
        validatorComboBox = QComboBox()
        validatorComboBox.addItem("No validator")
        validatorComboBox.addItem("Integer validator")
        validatorComboBox.addItem("Double validator")

        self.validatorLineEdit = QLineEdit()
        self.validatorLineEdit.setPlaceholderText("Placeholder Text")

        # signal & slot
        validatorComboBox.activated.connect(self.validatorChanged)

        # layout
        validatorLayout = QGridLayout()
        validatorLayout.addWidget(validatorLabel, 0, 0)
        validatorLayout.addWidget(validatorComboBox, 0, 1)
        validatorLayout.addWidget(self.validatorLineEdit, 1, 0, 1, 2)
        validatorGroup.setLayout(validatorLayout)

        return validatorGroup

    def validatorChanged(self, index: int):
        if index == 0:
            self.validatorLineEdit.setValidator(None)
        elif index == 1:
            intValidator = QIntValidator(self.validatorLineEdit)
            self.validatorLineEdit.setValidator(intValidator)
        elif index == 2:
            dblValidator = QDoubleValidator(-999.0, 999.0, 2, self.validatorLineEdit)
            self.validatorLineEdit.setValidator(dblValidator)
        self.validatorLineEdit.clear()

    def createAlignmentGroup(self):
        alignmentGroup = QGroupBox("Alignment")

        alignmentLabel = QLabel("Type:")
        alignmentComboBox = QComboBox()
        alignmentComboBox. addItem("Left")
        alignmentComboBox. addItem("Centered")
        alignmentComboBox. addItem("Right")

        self.alignmentLineEdit = QLineEdit()
        self.alignmentLineEdit.setPlaceholderText("Placeholder Text")

        # signal & slot
        alignmentComboBox.activated.connect(self.alignmentChanged)

        # layout
        alignmentLayout = QGridLayout()
        alignmentLayout.addWidget(alignmentLabel, 0, 0)
        alignmentLayout.addWidget(alignmentComboBox, 0, 1)
        alignmentLayout.addWidget(self.alignmentLineEdit, 1, 0, 1, 2)
        alignmentGroup.setLayout(alignmentLayout)

        return alignmentGroup

    def alignmentChanged(self, index: int):
        if index == 0:
            self.alignmentLineEdit.setAlignment(Qt.AlignLeft)
        elif index == 1:
            self.alignmentLineEdit.setAlignment(Qt.AlignCenter)
        elif index == 2:
            self.alignmentLineEdit.setAlignment(Qt.AlignRight)

    def createInputMaskGroup(self):
        inputMaskGroup = QGroupBox("Input mask")

        inputMaskLabel = QLabel("Type:")
        inputMaskComboBox = QComboBox()
        inputMaskComboBox.addItem("No mask")
        inputMaskComboBox.addItem("Phone number")
        inputMaskComboBox.addItem("ISO date")
        inputMaskComboBox.addItem("License key")

        self.inputMaskLineEdit = QLineEdit()
        self.inputMaskLineEdit.setPlaceholderText("Placeholder Text")

        # signal & slot
        inputMaskComboBox.activated.connect(self.inputMaskChanged)

        # layout
        inputMaskLayout = QGridLayout()
        inputMaskLayout.addWidget(inputMaskLabel, 0, 0)
        inputMaskLayout.addWidget(inputMaskComboBox, 0, 1)
        inputMaskLayout.addWidget(self.inputMaskLineEdit, 1, 0, 1, 2)
        inputMaskGroup.setLayout(inputMaskLayout)

        return inputMaskGroup

    def inputMaskChanged(self, index: int):
        if index == 0:
            self.inputMaskLineEdit.setInputMask("")
        elif index == 1:
            self.inputMaskLineEdit.setInputMask("+99 999 999 9999")
        elif index == 2:
            self.inputMaskLineEdit.setInputMask("0000-00-00")
            self.inputMaskLineEdit.setText("00000000")
            self.inputMaskLineEdit.setCursorPosition(0)
        elif index == 3:
            self.inputMaskLineEdit.setInputMask(">AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#")

    def createAccessGroup(self):
        accessGroup = QGroupBox("Access")

        accessLabel = QLabel("Read-only:")
        accessComboBox = QComboBox()
        accessComboBox.addItem("False")
        accessComboBox.addItem("True")

        self.accessLineEdit = QLineEdit()
        self.accessLineEdit.setPlaceholderText("Placeholder Text")

        # signal & slot
        accessComboBox.activated.connect(self.accessChanged)

        # layout
        accessLayout = QGridLayout()
        accessLayout.addWidget(accessLabel, 0, 0)
        accessLayout.addWidget(accessComboBox, 0, 1)
        accessLayout.addWidget(self.accessLineEdit, 1, 0, 1, 2)
        accessGroup.setLayout(accessLayout)

        return accessGroup

    def accessChanged(self, index: int):
        readOnly: bool = (index == 1)
        self.accessLineEdit.setReadOnly(readOnly)


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = ChocolafApp(sys.argv)

    win = Window()
    win.setStyleSheet(app.getStyleSheet("Chocolaf"))
    win.setWindowTitle('PyQt LineEdits - Chocolaf Theme')
    win.move(100, 100)
    win.show()

    rect = win.geometry()
    win1 = Window()
    win1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    win1.setWindowTitle('PyQt LineEdits - QDarkStyle(dark) Theme')
    win1.move(rect.left() + rect.width() + 100, rect.top() + 50)
    win1.show()

    return app.exec()


if __name__ == "__main__":
    main()
