"""
* spinBoxes.py: PyQt version of the spinboxes Qt Widgets demo using Chocolaf theme
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

# sys.path.append(os.path.join(pathlib.Path(__file__).absolute().parents[2], 'common_files'))
# from pyqt5_utils import ChocolafApp
import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp


class Window(QWidget):
    def __init__(self, parent: QWidget = None):
        super(Window, self).__init__(parent)

        spinBoxesGroup = self.createSpinBoxes()
        dateTimeEditsGroup = self.createDateTimeEdits()
        doubleSpinBoxesGroup = self.createDoubleSpinBoxes()
        closeBtn = QPushButton("Close")
        closeBtn.clicked.connect(qApp.exit)

        btnLayout = QHBoxLayout()
        btnLayout.addStretch()
        btnLayout.addWidget(closeBtn)

        mainLayout = QVBoxLayout()

        groupsLayout = QHBoxLayout()
        groupsLayout.addWidget(spinBoxesGroup)
        groupsLayout.addWidget(dateTimeEditsGroup)
        groupsLayout.addWidget(doubleSpinBoxesGroup)

        mainLayout.addLayout(groupsLayout)
        mainLayout.addLayout(btnLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("SpinBoxes Demo")

    def createSpinBoxes(self):
        spinBoxesGroup = QGroupBox("Spinboxes")

        integerLabel = QLabel(f"Enter value beteween {-20} and {20}")
        integerSpinBox = QSpinBox()
        integerSpinBox.setRange(-20, 20)
        integerSpinBox.setSingleStep(1)
        integerSpinBox.setValue(0)
        integerLabel.setBuddy(integerSpinBox)

        zoomLabel = QLabel(f"Enter zoom value between {0} and {1000}")
        zoomSpinBox = QSpinBox()
        zoomSpinBox.setRange(0, 1000)
        zoomSpinBox.setSingleStep(10)
        zoomSpinBox.setSuffix("%")
        zoomSpinBox.setSpecialValueText("Automatic")
        zoomSpinBox.setValue(100)
        zoomLabel.setBuddy(zoomSpinBox)

        priceLabel = QLabel(f"Enter price between {0} and {999}")
        priceSpinBox = QSpinBox()
        priceSpinBox.setRange(0, 999)
        priceSpinBox.setSingleStep(1)
        priceSpinBox.setPrefix("$")
        priceSpinBox.setValue(99)
        priceLabel.setBuddy(priceSpinBox)

        hexLabel = QLabel(f"Enter value between -{hex(31)} and {hex(31)}")
        hexSpinBox = QSpinBox()
        hexSpinBox.setRange(-31, 31)
        hexSpinBox.setSingleStep(1)
        hexSpinBox.setValue(0)
        hexSpinBox.setDisplayIntegerBase(16)
        hexLabel.setBuddy(hexSpinBox)

        groupSeparatorCheck = QCheckBox("Show separator")
        groupSeparatorSpinBox = QSpinBox()
        groupSeparatorCheck.toggled.connect(groupSeparatorSpinBox.setGroupSeparatorShown)
        groupSeparatorCheck.setChecked(True)
        groupSeparatorSpinBox.setRange(-99999999, 99999999)
        groupSeparatorSpinBox.setValue(1000)
        groupSeparatorSpinBox.setGroupSeparatorShown(True)

        spinBoxLayout = QVBoxLayout()
        spinBoxLayout.addWidget(integerLabel)
        spinBoxLayout.addWidget(integerSpinBox)
        spinBoxLayout.addWidget(zoomLabel)
        spinBoxLayout.addWidget(zoomSpinBox)
        spinBoxLayout.addWidget(priceLabel)
        spinBoxLayout.addWidget(priceSpinBox)
        spinBoxLayout.addWidget(hexLabel)
        spinBoxLayout.addWidget(hexSpinBox)
        spinBoxLayout.addWidget(groupSeparatorCheck)
        spinBoxLayout.addWidget(groupSeparatorSpinBox)
        spinBoxesGroup.setLayout(spinBoxLayout)

        return spinBoxesGroup

    def createDateTimeEdits(self):
        editsGroup = QGroupBox("Date and time spin boxes")

        dateLabel = QLabel()
        dateEdit = QDateEdit(QDate.currentDate())
        dateEdit.setDateRange(QDate(2010, 1, 1), QDate(2030, 12, 31))
        dateLabel.setText(f"Appointment date (between {dateEdit.minimumDate().toString(Qt.ISODate)} " +
                          f"and {dateEdit.maximumDate().toString(Qt.ISODate)})")
        dateLabel.setBuddy(dateEdit)

        timeLabel = QLabel()
        timeEdit = QTimeEdit(QTime.currentTime())
        # appointments available between 9AM and 5:30 PM
        timeEdit.setTimeRange(QTime(9, 0, 0, 0), QTime(17, 30, 0, 0))
        timeLabel.setText(f"Appointments (between {timeEdit.minimumTime().toString(Qt.ISODate)} " +
                          f"and {timeEdit.maximumTime().toString(Qt.ISODate)})")
        timeLabel.setBuddy(timeEdit)

        self.meetingLabel = QLabel()
        self.meetingEdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.meetingLabel.setBuddy(self.meetingEdit)

        formatLabel = QLabel(f"Format string for meeting date & time")
        self.formatComboBox = QComboBox()
        self.formatComboBox.addItem("yyyy-MM-dd hh:mm:ss (zzz 'ms')")
        self.formatComboBox.addItem("hh:mm:ss MM/dd/yyyy")
        self.formatComboBox.addItem("hh:mm:ss dd/MM/yyyy")
        self.formatComboBox.addItem("hh:mm:ss")
        self.formatComboBox.addItem("hh:mm ap")
        self.formatComboBox.textActivated.connect(self.setFormatString)
        self.setFormatString(self.formatComboBox.currentText())
        formatLabel.setBuddy(self.formatComboBox)

        editsLayout = QVBoxLayout()
        editsLayout.addWidget(dateLabel)
        editsLayout.addWidget(dateEdit)
        editsLayout.addWidget(timeLabel)
        editsLayout.addWidget(timeEdit)
        editsLayout.addWidget(self.meetingLabel)
        editsLayout.addWidget(self.meetingEdit)
        editsLayout.addWidget(formatLabel)
        editsLayout.addWidget(self.formatComboBox)

        editsGroup.setLayout(editsLayout)
        return editsGroup

    def setFormatString(self, formatString: str):
        self.meetingEdit.setDisplayFormat(formatString)
        if (self.meetingEdit.displayedSections() and QDateTimeEdit.Section.DateSections_Mask):
            self.meetingEdit.setDateRange(QDate(2022, 1, 1), QDate(2022, 3, 31))
            self.meetingLabel.setText(f"Meeting date (between {self.meetingEdit.minimumDate().toString(Qt.ISODate)} " +
                                      f"and {self.meetingEdit.maximumDate().toString(Qt.ISODate)})")
        else:
            self.meetingEdit.setTimeRange(QTime(0, 7, 20, 0), QTime(21, 0, 0, 0))
            self.meetingLabel.setText(f"Meeting time (between {self.meetingEdit.minimumTime().toString(Qt.ISODate)} " +
                                      f"and {self.meetingEdit.maximumTime().toString(Qt.ISODate)})")

    def createDoubleSpinBoxes(self):
        doubleSpinBoxesGroup = QGroupBox("Double precision spinboxes")

        precisionLabel = QLabel(f"Number of decimal places to show:")
        precisionSpinBox = QSpinBox()
        precisionSpinBox.setRange(0, 100)
        precisionSpinBox.setValue(2)
        precisionLabel.setBuddy(precisionSpinBox)
        precisionSpinBox.valueChanged.connect(self.changePrecision)

        doubleLabel = QLabel(f"Enter value between {-20} and {20}")
        self.doubleSpinBox = QDoubleSpinBox()
        self.doubleSpinBox.setRange(-20, 20)
        self.doubleSpinBox.setSingleStep(1.0)
        self.doubleSpinBox.setValue(0.0)
        doubleLabel.setBuddy(self.doubleSpinBox)

        scaleLabel = QLabel(f"Enter scale factor between {0.0} and {1000.0}")
        self.scaleSpinBox = QDoubleSpinBox()
        self.scaleSpinBox.setRange(0.0, 1000.0)
        self.scaleSpinBox.setSingleStep(10.0)
        self.scaleSpinBox.setSuffix("%")
        self.scaleSpinBox.setSpecialValueText("No scaling")
        self.scaleSpinBox.setValue(100.0)
        scaleLabel.setBuddy(self.scaleSpinBox)

        priceLabel = QLabel(f"Enter price between {0} and {1000}")
        self.priceSpinBox = QDoubleSpinBox()
        self.priceSpinBox.setRange(0.0, 1000.0)
        self.priceSpinBox.setSingleStep(1.0)
        self.priceSpinBox.setPrefix("$")
        self.priceSpinBox.setValue(99.99)
        priceLabel.setBuddy(self.priceSpinBox)

        groupSepartorLabel = QLabel("Show group separator (~QCheckBox)")
        groupSeparatorSpinBox = QDoubleSpinBox()
        groupSeparatorSpinBox.setRange(-99999999, 99999999)
        groupSeparatorSpinBox.setDecimals(2)
        groupSeparatorSpinBox.setValue(1000.0)
        groupSeparatorSpinBox.setGroupSeparatorShown(True)

        spinBoxLayout = QVBoxLayout()
        spinBoxLayout.addWidget(precisionLabel)
        spinBoxLayout.addWidget(precisionSpinBox)
        spinBoxLayout.addWidget(doubleLabel)
        spinBoxLayout.addWidget(self.doubleSpinBox)
        spinBoxLayout.addWidget(scaleLabel)
        spinBoxLayout.addWidget(self.scaleSpinBox)
        spinBoxLayout.addWidget(priceLabel)
        spinBoxLayout.addWidget(self.priceSpinBox)
        spinBoxLayout.addWidget(groupSepartorLabel)
        spinBoxLayout.addWidget(groupSeparatorSpinBox)

        doubleSpinBoxesGroup.setLayout(spinBoxLayout)
        return doubleSpinBoxesGroup

    def changePrecision(self, decimals: int):
        self.doubleSpinBox.setDecimals(decimals)
        self.scaleSpinBox.setDecimals(decimals)
        self.priceSpinBox.setDecimals(decimals)


def loadStyleSheet() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    print(f"loadStyleSheet() . You are {here}")
    darkss_dir = os.path.join(here, "styles", "dark")
    sys.path.append(darkss_dir)
    import stylesheet_rc

    darkss_path = os.path.join(darkss_dir, "stylesheet.css")
    assert os.path.exists(darkss_path)
    print(f"LoadStyleSheet() . loading dark stylesheet from {darkss_path}")
    stylesheet = ""
    with open(darkss_path, "r") as f:
        stylesheet = f.read()
    return stylesheet


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = ChocolafApp(sys.argv)

    win = Window()
    win.setStyleSheet(app.getStyleSheet("Chocolaf"))
    win.move(50, 50)
    win.show()

    rect = win.geometry()
    win1 = Window()
    win1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    win1.move(rect.left() + rect.width() // 2 + 20, rect.top() + rect.height() + 10)
    win1.show()

    return app.exec()


if __name__ == "__main__":
    main()
