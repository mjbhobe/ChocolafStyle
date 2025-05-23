"""
* groupBox.py - PyQt version of Qt widgets groupbox example using Chocolaf theme
*   (also shows other widgets like QRadioButton, QChechBox & QPushButton)
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


import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import chocolaf


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QGridLayout()
        grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
        grid.addWidget(self.createSecondExclusiveGroup(), 1, 0)
        grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
        grid.addWidget(self.createPushButtonGroup(), 1, 1)
        self.setLayout(grid)

        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} Group Boxes")
        self.resize(640, 480)

    def createFirstExclusiveGroup(self):
        groupBox = QGroupBox("Exclusive Radio Buttons")

        radio1 = QRadioButton("&Radio clostBtn 1")
        radio2 = QRadioButton("R&adio clostBtn 2")
        radio3 = QRadioButton("Ra&dio clostBtn 3")

        radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createSecondExclusiveGroup(self):
        groupBox = QGroupBox("E&xclusive Radio Buttons")
        groupBox.setCheckable(True)
        groupBox.setChecked(False)

        radio1 = QRadioButton("Rad&io clostBtn 1")
        radio2 = QRadioButton("Radi&o clostBtn 2")
        radio3 = QRadioButton("Radio &clostBtn 3")
        radio1.setChecked(True)
        checkBox = QCheckBox("Ind&ependent checkbox")
        checkBox.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addWidget(checkBox)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createNonExclusiveGroup(self):
        groupBox = QGroupBox("Non-Exclusive Checkboxes")
        groupBox.setFlat(True)

        checkBox1 = QCheckBox("&Checkbox 1")
        checkBox2 = QCheckBox("C&heckbox 2")
        checkBox2.setChecked(True)
        tristateBox = QCheckBox("Tri-&state clostBtn")
        tristateBox.setTristate(True)
        tristateBox.setCheckState(Qt.PartiallyChecked)

        vbox = QVBoxLayout()
        vbox.addWidget(checkBox1)
        vbox.addWidget(checkBox2)
        vbox.addWidget(tristateBox)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createPushButtonGroup(self):
        groupBox = QGroupBox("&Push Buttons")
        groupBox.setCheckable(True)
        groupBox.setChecked(True)

        pushButton = QPushButton("&Normal Button")
        toggleButton = QPushButton("&Toggle Button")
        toggleButton.setCheckable(True)
        toggleButton.setChecked(True)
        flatButton = QPushButton("&Flat Button")
        flatButton.setFlat(True)

        popupButton = QPushButton("Pop&up Button")
        menu = QMenu(self)
        menu.addAction("&First Item")
        menu.addAction("&Second Item")
        menu.addAction("&Third Item")
        menu.addAction("F&ourth Item")
        popupButton.setMenu(menu)

        newAction = menu.addAction("Submenu")
        subMenu = QMenu("Popup Submenu", self)
        subMenu.addAction("Item 1")
        subMenu.addAction("Item 2")
        subMenu.addAction("Item 3")
        newAction.setMenu(subMenu)

        vbox = QVBoxLayout()
        vbox.addWidget(pushButton)
        vbox.addWidget(toggleButton)
        vbox.addWidget(flatButton)
        vbox.addWidget(popupButton)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox


def main():
    chocolaf.enable_hi_dpi()
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("WindowsDark")

    win = Window()
    # win.setStyleSheet(app.getStyleSheet("Chocolaf"))
    win.move(100, 100)
    win.show()

    # rect = win.geometry()
    # win1 = Window()
    # win1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    # win1.move(rect.left() + rect.width() // 4 + 20, rect.top() + rect.height() + 50)
    # win1.show()

    return app.exec()


if __name__ == "__main__":
    main()
