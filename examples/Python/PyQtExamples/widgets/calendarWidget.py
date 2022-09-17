"""
* calendarWidget.py: PyQt5 version of the Qt calendar widgets demo using Chocolaf theme
*   (NOTE: not themed fully yet!)
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
        self.previewGroupBox: QGroupBox = QGroupBox("Preview")
        self.calendar: QCalendarWidget = QCalendarWidget()

        self.generalOptionsGroupBox = QGroupBox("General Options")
        self.localeCombo = QComboBox()
        self.localeLabel = QLabel("&Locale:")
        self.localeLabel.setBuddy(self.localeCombo)
        self.firstDayCombo = QComboBox()
        self.firstDayLabel = QLabel("Wee&k starts on:")
        self.firstDayLabel.setBuddy(self.firstDayCombo)
        self.selectionModeCombo = QComboBox()
        self.selectionModeLabel = QLabel("Selection mode:")
        self.selectionModeLabel.setBuddy(self.selectionModeCombo)
        self.gridCheckBox = QCheckBox("&Grid")
        self.gridCheckBox.setChecked(True)
        self.navigationCheckBox = QCheckBox("&Navigation bar")
        self.navigationCheckBox.setChecked(True)
        self.horizontalHeaderCombo = QComboBox()
        self.horizontalHeaderLabel = QLabel("&Horizontal header:")
        self.horizontalHeaderLabel.setBuddy(self.horizontalHeaderCombo)
        self.verticalHeaderCombo = QComboBox()
        self.verticalHeaderLabel = QLabel("&Vertical header:")
        self.verticalHeaderLabel.setBuddy(self.verticalHeaderCombo)

        self.datesGroupBox = self.createDatesGroupBox()

        self.textFormatsGroupBox = QGroupBox("Text Formats")
        self.weekdayColorCombo = self.createColorComboBox()
        self.weekdayColorCombo.setCurrentIndex(self.weekdayColorCombo.findText("White"))
        self.weekdayColorLabel = QLabel("&Weekday color:")
        self.weekdayColorLabel.setBuddy(self.weekdayColorCombo)
        self.weekendColorCombo = self.createColorComboBox()
        self.weekendColorCombo.setCurrentIndex(self.weekendColorCombo.findText("Red"))
        self.weekendColorLabel = QLabel("Week&end color:")
        self.weekendColorLabel.setBuddy(self.weekendColorCombo)
        self.headerTextFormatCombo = QComboBox()
        self.headerTextFormatCombo.addItem("Bold")
        self.headerTextFormatCombo.addItem("Italic")
        self.headerTextFormatCombo.addItem("Plain")
        self.headerTextFormatLabel = QLabel("&Header text:")
        self.headerTextFormatLabel.setBuddy(self.headerTextFormatCombo)
        self.firstFridayCheckBox = QCheckBox("&First Friday in blue")
        self.mayFirstCheckBox = QCheckBox("May &1 in red")

        self.setupUi()
        self.setWindowTitle("Calendar Widget Demo")

    def setupUi(self):
        self.createPreviewGroupBox()
        self.createGeneralOptionsGroupBox()
        self.createTextFormatsGroupBox()

        layout = QGridLayout()
        layout.addWidget(self.previewGroupBox, 0, 0)
        layout.addWidget(self.generalOptionsGroupBox, 0, 1)
        layout.addWidget(self.datesGroupBox, 1, 0)
        layout.addWidget(self.textFormatsGroupBox, 1, 1)
        self.setLayout(layout)

    def createPreviewGroupBox(self):
        self.calendar.setMinimumDate(QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QDate(3000, 1, 1))
        self.calendar.setGridVisible(True)
        self.calendar.currentPageChanged.connect(self.reformatCalendarPage)
        self.previewLayout = QGridLayout()
        self.previewLayout.addWidget(self.calendar, 0, 0, Qt.AlignCenter)
        self.previewGroupBox.setLayout(self.previewLayout)

    def createGeneralOptionsGroupBox(self):
        currLocaleIndex, index = -1, 0
        for i in range(int(QLocale.Language.C), int(QLocale.Language.LastLanguage)):
            lang: QLocale.Language = QLocale.Language(i)
            langLocales = QLocale.matchingLocales(lang, QLocale.AnyScript, QLocale.AnyCountry)
            for langLocale in langLocales:
                label = QLocale.languageToString(lang)
                label = label + '/'
                label = label + QLocale.countryToString(langLocale.country())
                locale: QLocale = QLocale(lang, langLocale.country())
                if (self.locale().language() == lang) and (self.locale().country() == langLocale.country()):
                    currLocaleIndex = index
                self.localeCombo.addItem(label, locale)
                index += 1
        if currLocaleIndex != -1:
            self.localeCombo.setCurrentIndex(currLocaleIndex)

        # Issue: these should come from self.locale()
        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        weekdays_code = [Qt.Sunday, Qt.Monday, Qt.Tuesday, Qt.Wednesday, Qt.Thursday, Qt.Friday, Qt.Saturday]

        for w, wc in zip(weekdays, weekdays_code):
            self.firstDayCombo.addItem(w, wc)

        self.selectionModeCombo.addItem("Single Selection", QCalendarWidget.SingleSelection)
        self.selectionModeCombo.addItem("None", QCalendarWidget.NoSelection)

        self.horizontalHeaderCombo.addItem("Single letter day names", QCalendarWidget.SingleLetterDayNames)
        self.horizontalHeaderCombo.addItem("Short day names", QCalendarWidget.ShortDayNames)
        self.horizontalHeaderCombo.addItem("None", QCalendarWidget.NoHorizontalHeader)
        self.horizontalHeaderCombo.setCurrentIndex(1)

        self.verticalHeaderCombo.addItem("ISO week numbers", QCalendarWidget.ISOWeekNumbers)
        self.verticalHeaderCombo.addItem("None", QCalendarWidget.NoVerticalHeader)

        self.localeCombo.currentIndexChanged.connect(self.localeChanged)
        self.firstDayCombo.currentIndexChanged.connect(self.firstDayChanged)
        self.selectionModeCombo.currentIndexChanged.connect(self.selectionModeChanged)
        self.gridCheckBox.toggled.connect(self.calendar.setGridVisible)
        self.navigationCheckBox.toggled.connect(self.calendar.setNavigationBarVisible)
        self.horizontalHeaderCombo.currentIndexChanged.connect(self.horizontalHeaderChanged)
        self.verticalHeaderCombo.currentIndexChanged.connect(self.verticalHeaderChanged)

        # layout the controls
        checkBoxLayout = QHBoxLayout()
        checkBoxLayout.addWidget(self.gridCheckBox)
        checkBoxLayout.addStretch()
        checkBoxLayout.addWidget(self.navigationCheckBox)

        self.outerLayout = QGridLayout()
        self.outerLayout.addWidget(self.localeLabel, 0, 0)
        self.outerLayout.addWidget(self.localeCombo, 0, 1)
        self.outerLayout.addWidget(self.firstDayLabel, 1, 0)
        self.outerLayout.addWidget(self.firstDayCombo, 1, 1)
        self.outerLayout.addWidget(self.selectionModeLabel, 2, 0)
        self.outerLayout.addWidget(self.selectionModeCombo, 2, 1)
        self.outerLayout.addLayout(checkBoxLayout, 3, 0, 1, 2)
        self.outerLayout.addWidget(self.horizontalHeaderLabel, 4, 0)
        self.outerLayout.addWidget(self.horizontalHeaderCombo, 4, 1)
        self.outerLayout.addWidget(self.verticalHeaderLabel, 5, 0)
        self.outerLayout.addWidget(self.verticalHeaderCombo, 5, 1)
        self.generalOptionsGroupBox.setLayout(self.outerLayout)

        self.firstDayChanged(self.firstDayCombo.currentIndex())
        self.selectionModeChanged(self.selectionModeCombo.currentIndex())
        self.horizontalHeaderChanged(self.horizontalHeaderCombo.currentIndex())
        self.verticalHeaderChanged(self.verticalHeaderCombo.currentIndex())

    def createColorComboBox(self) -> QComboBox:
        comboBox: QComboBox = QComboBox()
        comboBox.addItem("Red", QColor(Qt.red))
        comboBox.addItem("Salmon", QColor(191, 97, 106))
        comboBox.addItem("Orange", QColor(208, 135, 112))
        comboBox.addItem("Yellow", QColor(235, 203, 115))
        comboBox.addItem("Green", QColor(163, 190, 140))
        comboBox.addItem("Pink", QColor(180, 142, 173))
        comboBox.addItem("White", QColor(Qt.white))
        return comboBox

    def createDatesGroupBox(self):
        datesGroupBox: QGroupBox = QGroupBox("Dates")

        self.minimumDateEdit = QDateEdit()
        self.minimumDateEdit.setDisplayFormat("MMM d yyyy")
        self.minimumDateEdit.setDateRange(self.calendar.minimumDate(), self.calendar.maximumDate())
        self.minimumDateEdit.setDate(self.calendar.minimumDate())

        self.minimumDateLabel = QLabel("&Minimum Date:")
        self.minimumDateLabel.setBuddy(self.minimumDateEdit)

        self.currentDateEdit = QDateEdit()
        self.currentDateEdit.setDisplayFormat("MMM d yyyy")
        self.currentDateEdit.setDate(self.calendar.selectedDate())
        self.currentDateEdit.setDateRange(self.calendar.minimumDate(), self.calendar.maximumDate())

        self.currentDateLabel = QLabel("&Current Date:")
        self.currentDateLabel.setBuddy(self.currentDateEdit)

        self.maximumDateEdit = QDateEdit()
        self.maximumDateEdit.setDisplayFormat("MMM d yyyy")
        self.maximumDateEdit.setDateRange(self.calendar.minimumDate(), self.calendar.maximumDate())
        self.maximumDateEdit.setDate(self.calendar.maximumDate())

        self.maximumDateLabel = QLabel("Ma&ximum Date:")
        self.maximumDateLabel.setBuddy(self.maximumDateEdit)

        self.currentDateEdit.dateChanged.connect(self.calendar.setSelectedDate)
        self.calendar.selectionChanged.connect(self.selectedDateChanged)
        self.minimumDateEdit.dateChanged.connect(self.minimumDateChanged)
        self.maximumDateEdit.dateChanged.connect(self.maximumDateChanged)

        self.dateBoxLayout = QGridLayout()
        self.dateBoxLayout.addWidget(self.currentDateLabel, 1, 0)
        self.dateBoxLayout.addWidget(self.currentDateEdit, 1, 1)
        self.dateBoxLayout.addWidget(self.minimumDateLabel, 0, 0)
        self.dateBoxLayout.addWidget(self.minimumDateEdit, 0, 1)
        self.dateBoxLayout.addWidget(self.maximumDateLabel, 2, 0)
        self.dateBoxLayout.addWidget(self.maximumDateEdit, 2, 1)
        self.dateBoxLayout.setRowStretch(3, 1)

        datesGroupBox.setLayout(self.dateBoxLayout)

        return datesGroupBox

    def selectedDateChanged(self):
        self.currentDateEdit.setDate(self.calendar.selectedDate())

    def minimumDateChanged(self, date: QDate):
        self.calendar.setMinimumDate(date)
        self.maximumDateEdit.setDate(self.calendar.maximumDate())

    def maximumDateChanged(self, date: QDate):
        self.calendar.setMaximumDate(date)
        self.minimumDateEdit.setDate(self.calendar.minimumDate())

    def createTextFormatsGroupBox(self):
        # setup layout for text format group box (all widgets created in constructor)
        self.weekdayColorCombo.currentIndexChanged.connect(self.weekdayFormatChanged)
        self.weekdayColorCombo.currentIndexChanged.connect(self.reformatCalendarPage)
        self.weekendColorCombo.currentIndexChanged.connect(self.weekendFormatChanged)
        self.weekendColorCombo.currentIndexChanged.connect(self.reformatCalendarPage)
        self.headerTextFormatCombo.currentIndexChanged.connect(self.reformatHeaders)
        self.firstFridayCheckBox.toggled.connect(self.reformatCalendarPage)
        self.mayFirstCheckBox.toggled.connect(self.reformatCalendarPage)

        checkBoxLayout = QHBoxLayout()
        checkBoxLayout.addWidget(self.firstFridayCheckBox)
        checkBoxLayout.addStretch()
        checkBoxLayout.addWidget(self.mayFirstCheckBox)

        outerLayout = QGridLayout()
        outerLayout.addWidget(self.weekdayColorLabel, 0, 0)
        outerLayout.addWidget(self.weekdayColorCombo, 0, 1)
        outerLayout.addWidget(self.weekendColorLabel, 1, 0)
        outerLayout.addWidget(self.weekendColorCombo, 1, 1)
        outerLayout.addWidget(self.headerTextFormatLabel, 2, 0)
        outerLayout.addWidget(self.headerTextFormatCombo, 2, 1)
        outerLayout.addLayout(checkBoxLayout, 3, 0, 1, 2)
        self.textFormatsGroupBox.setLayout(outerLayout)
        self.weekdayFormatChanged()
        self.weekendFormatChanged()
        self.reformatHeaders()
        self.reformatCalendarPage()

    def weekdayFormatChanged(self):
        format = QTextCharFormat()
        format.setForeground(QColor(self.weekdayColorCombo.itemData(self.weekdayColorCombo.currentIndex())))
        self.calendar.setWeekdayTextFormat(Qt.Monday, format)
        self.calendar.setWeekdayTextFormat(Qt.Tuesday, format)
        self.calendar.setWeekdayTextFormat(Qt.Wednesday, format)
        self.calendar.setWeekdayTextFormat(Qt.Thursday, format)
        self.calendar.setWeekdayTextFormat(Qt.Friday, format)

    def weekendFormatChanged(self):
        format = QTextCharFormat()
        format.setForeground(QColor(self.weekendColorCombo.itemData(self.weekendColorCombo.currentIndex())))
        self.calendar.setWeekdayTextFormat(Qt.Saturday, format)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, format)

    def reformatHeaders(self):
        text = self.headerTextFormatCombo.currentText()
        format = QTextCharFormat()

        if (text == "Bold"):
            format.setFontWeight(QFont.Bold)
        elif (text == "Italic"):
            format.setFontItalic(True)
        self.calendar.setHeaderTextFormat(format)

    def reformatCalendarPage(self):
        defaultForeground: QColor = QColor(self.weekdayColorCombo.itemData(self.weekdayColorCombo.currentIndex()))

        firstFridayFormat = QTextCharFormat()
        firstFriday: QDate = QDate(self.calendar.yearShown(), self.calendar.monthShown(), 1)
        while (firstFriday.dayOfWeek() != Qt.Friday):
            firstFriday = firstFriday.addDays(1)

        if self.firstFridayCheckBox.isChecked():
            firstFridayFormat.setForeground(QColor(0, 114, 198))
            firstFridayFormat.setFontWeight(QFont.Bold)
        else:
            # revert to default format
            firstFridayFormat.setForeground(defaultForeground)
        self.calendar.setDateTextFormat(firstFriday, firstFridayFormat)

        mayFirstFormat = QTextCharFormat()
        mayFirst: QDate = QDate(self.calendar.yearShown(), 5, 1)

        if self.mayFirstCheckBox.isChecked():
            mayFirstFormat.setForeground(QColor(180, 142, 173))
        elif ((not self.firstFridayCheckBox.isChecked()) or (firstFriday != mayFirst)):
            dayOfWeek = mayFirst.dayOfWeek()
            self.calendar.setDateTextFormat(mayFirst, self.calendar.weekdayTextFormat(dayOfWeek))

    def localeChanged(self, index: int):
        itemLocale: QLocale = self.localeCombo.itemData(index)
        newLocale: QLocale = QLocale(itemLocale.language(), itemLocale.script(), itemLocale.country())
        self.calendar.setLocale(newLocale)
        newLocaleFirstDayIndex = self.firstDayCombo.findData(newLocale.firstDayOfWeek())
        self.firstDayCombo.setCurrentIndex(newLocaleFirstDayIndex)

    def firstDayChanged(self, index: int):
        self.calendar.setFirstDayOfWeek(Qt.DayOfWeek(int(self.firstDayCombo.itemData(index))))

    def selectionModeChanged(self, index: int):
        self.calendar.setSelectionMode(QCalendarWidget.SelectionMode(int(self.selectionModeCombo.itemData(index))))

    def horizontalHeaderChanged(self, index: int):
        self.calendar.setHorizontalHeaderFormat(
            QCalendarWidget.HorizontalHeaderFormat(int(self.horizontalHeaderCombo.itemData(index))))

    def verticalHeaderChanged(self, index: int):
        self.calendar.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat(int(self.verticalHeaderCombo.itemData(index))))


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
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = ChocolafApp(sys.argv)

    win = Window()
    win.setStyleSheet(app.getStyleSheet("Chocolaf"))
    win.move(100, 100)
    win.show()

    rect = win.geometry()
    win1 = Window()
    win1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    win1.move(rect.left() + rect.width() // 4 + 20, rect.top() + rect.height() + 10)
    win1.show()

    return app.exec()


if __name__ == "__main__":
    main()
