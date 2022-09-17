#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* widgetGallery.py: demonstrates PyQt5 widget gallery
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
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from sklearn.manifold import trustworthiness

import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp


class WidgetGallery(QWidget):
    def __init__(self, parent: QWidget = None):
        super(WidgetGallery, self).__init__(parent)
        self.buttonsGroupBox = self.createButtonsGroupBox()
        self.itemViewTabWidget = self.createItemViewTabWidget()
        self.simpleWidgetsGroupBox = self.createSimpleWidgetsGroupBox()
        self.toolBox = self.createTextToolBox()

        closeBtn = QPushButton("Close")
        closeBtn.setToolTip("Close the application")
        closeLayout = QHBoxLayout()
        closeLayout.addStretch()
        closeLayout.addWidget(closeBtn)
        closeBtn.clicked.connect(qApp.exit)

        groupsLayout = QGridLayout()
        groupsLayout.addWidget(self.buttonsGroupBox, 0, 0)
        groupsLayout.addWidget(self.simpleWidgetsGroupBox, 0, 1)
        groupsLayout.addWidget(self.itemViewTabWidget, 1, 0)
        groupsLayout.addWidget(self.toolBox, 1, 1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(closeLayout)
        mainLayout.addLayout(groupsLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle("Qt Widgets Demo")

    def createButtonsGroupBox(self) -> QGroupBox:
        buttonsGroupBox = QGroupBox("Buttons")
        buttonsGroupBox.setCheckable(True)
        buttonsGroupBox.setChecked(True)

        defPushButton = QPushButton("Default Push Button")
        defPushButton.setDefault(True)
        regPushButton = QPushButton("Regular Push Button")
        disPushButton = QPushButton("Disabled Push Button")
        disPushButton.setEnabled(False)
        togglePushButton = QPushButton("Toggle Push Button")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)
        flatPushButton = QPushButton("Flat Push Button")
        flatPushButton.setFlat(True)

        toolButton = QToolButton()
        toolButton.setText("Tool Button")
        chkToolButton = QToolButton()
        chkToolButton.setText("Checkable TB")
        chkToolButton.setCheckable(True)
        menuToolButton = QToolButton()
        menuToolButton.setText("Menu Button")
        toolMenu = QMenu(menuToolButton)
        menuToolButton.setPopupMode(QToolButton.InstantPopup)
        action = QAction("Regular Option", self)
        action.setShortcut(QKeySequence.New)
        toolMenu.addAction(action)
        toolMenu.addSeparator()
        act = toolMenu.addAction("Checkable Option")
        act.setCheckable(True)
        menuToolButton.setMenu(toolMenu)

        toolLayout = QGridLayout()
        toolLayout.addWidget(toolButton, 0, 0)
        toolLayout.addWidget(chkToolButton, 0, 1)
        toolLayout.addWidget(menuToolButton, 1, 0, 1, 2)

        commandLinkButton = QCommandLinkButton("Command Link Button")
        commandLinkButton.setDescription("This is the description")

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(defPushButton)
        buttonLayout.addWidget(regPushButton)
        buttonLayout.addWidget(disPushButton)
        buttonLayout.addWidget(togglePushButton)
        buttonLayout.addWidget(flatPushButton)
        buttonLayout.addLayout(toolLayout)
        buttonLayout.addWidget(commandLinkButton)
        buttonLayout.addStretch(1)

        radioButton1 = QRadioButton("Radio Button 1")
        radioButton2 = QRadioButton("Radio Button 2")
        radioButton3 = QRadioButton("Radio Button 3")
        radioButton4 = QRadioButton("Disabled Radio")
        radioButton1.setChecked(True)
        radioButton4.setEnabled(False)
        checkBox1 = QCheckBox("Normal check box")
        checkBox1.setChecked(True)
        checkBox2 = QCheckBox("Disabled check box")
        checkBox2.setEnabled(False)
        checkBox3 = QCheckBox("Tri-state check box")
        checkBox3.setTristate(True)
        checkBox3.setCheckState(Qt.PartiallyChecked)

        checkableLayout = QVBoxLayout()
        checkableLayout.addWidget(radioButton1)
        checkableLayout.addWidget(radioButton2)
        checkableLayout.addWidget(radioButton3)
        checkableLayout.addWidget(radioButton4)
        checkableLayout.addWidget(checkBox1)
        checkableLayout.addWidget(checkBox2)
        checkableLayout.addWidget(checkBox3)
        checkableLayout.addStretch(1)

        groupLayout = QHBoxLayout()
        groupLayout.addLayout(buttonLayout)
        groupLayout.addLayout(checkableLayout)
        # groupLayout.addStretch(1)

        buttonsGroupBox.setLayout(groupLayout)
        return buttonsGroupBox

    def createSimpleWidgetsGroupBox(self):
        simpleWidgetsGroupBox = QGroupBox("Simple Input Widgets")
        simpleWidgetsGroupBox.setCheckable(True)
        simpleWidgetsGroupBox.setChecked(True)

        lineEdit = QLineEdit("Single Line Edit")
        lineEdit.setClearButtonEnabled(True)
        pwdEdit = QLineEdit("s3cRe7")
        pwdEdit.setClearButtonEnabled(True)
        pwdEdit.setEchoMode(QLineEdit.Password)
        spinBox = QSpinBox()
        spinBox.setRange(-200, 200)
        spinBox.setValue(50)
        dateTimeEdit = QDateTimeEdit(simpleWidgetsGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        slider = QSlider()
        slider.setOrientation(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(40)
        scrollBar = QScrollBar()
        scrollBar.setOrientation(Qt.Horizontal)
        scrollBar.setRange(0, 100)
        scrollBar.setValue(60)
        dial = QDial()
        dial.setValue(30)
        dial.setNotchesVisible(True)
        combo = QComboBox()
        items = ['Apple iPhone', 'OnePlus 9T', 'Dell XPS', 'Apple MacBook Pro',
                 'Python', 'Java', 'Spring', 'C/C++', 'Visual Studio Code', 'GNU C/C++',
                 'Vim', 'Tensorflow', 'Keras', 'Pytorch', 'Keras', 'Coffee']
        combo.addItems(items)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(pwdEdit, 1, 0, 1, 2)
        layout.addWidget(spinBox, 2, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 3, 0, 1, 2)
        layout.addWidget(slider, 4, 0)
        layout.addWidget(scrollBar, 5, 0)
        layout.addWidget(dial, 4, 1, 2, 1)
        layout.addWidget(combo, 6, 0, 1, 2)
        layout.setRowStretch(7, 1)
        simpleWidgetsGroupBox.setLayout(layout)

        return simpleWidgetsGroupBox

    def embedIntoHBoxLayout(self, widget: QWidget, margin: int = 5) -> QWidget:
        ret = QWidget()
        layout = QHBoxLayout(ret)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.addWidget(widget)
        return ret

    def createItemViewTabWidget(self) -> QTabWidget:
        result = QTabWidget()
        result.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        treeView = QTreeView()
        fileSystemModel = QFileSystemModel(treeView)
        fileSystemModel.setRootPath(QDir.rootPath())
        treeView.setModel(fileSystemModel)

        tableWidget = QTableWidget()
        tableWidget.setRowCount(10)
        tableWidget.setColumnCount(10)

        listModel = QStandardItemModel(0, 1, result)
        dirOpenIcon = QIcon(":/qt-project.org/styles/commonstyle/images/diropen-128.png")
        computerIcon = QIcon(":/qt-project.org/styles/commonstyle/images/computer-32.png")

        listModel.appendRow(QStandardItem(dirOpenIcon, "Directory"))
        listModel.appendRow(QStandardItem(computerIcon, "Compute"))

        listView = QListView()
        listView.setModel(listModel)

        iconModelListView = QListView()
        iconModelListView.setViewMode(QListView.IconMode)
        iconModelListView.setModel(listModel)

        result.addTab(self.embedIntoHBoxLayout(treeView), "&Tree View")
        result.addTab(self.embedIntoHBoxLayout(tableWidget), "T&able")
        result.addTab(self.embedIntoHBoxLayout(listView), "&List")
        result.addTab(self.embedIntoHBoxLayout(iconModelListView), "&Icon Model List")
        return result

    def createTextToolBox(self) -> QToolBox:
        textToolBox = QToolBox()

        plainText: str = ("Twinkle, twinkle, little star,\n" +
                          "How I wonder what you are.\n" +
                          "Up above the world so high,\n" +
                          "Like a diamond in the sky.\n" +
                          "Twinkle, twinkle, little star,\n" +
                          "How I wonder what you are!\n")

        richText = "<html><head/><body><i>"
        for line in plainText.split("\n"):
            richText += "<center>" + line + "</center>"
        richText += "</i></body></html>"
        print(richText)

        plainTextEdit = QPlainTextEdit(plainText)
        textEdit = QTextEdit(richText)
        self.systemInfoTextBrowser = QTextBrowser()
        self.updateSystemInfo()

        textToolBox.addItem(self.embedIntoHBoxLayout(plainTextEdit), "Plain Text Edit")
        textToolBox.addItem(self.embedIntoHBoxLayout(textEdit), "Text Edit")
        textToolBox.addItem(self.embedIntoHBoxLayout(self.systemInfoTextBrowser), "Text Browser")
        return textToolBox

    @ staticmethod
    def highDpiScaleFactorRoundingPolicy():
        policy = QGuiApplication.highDpiScaleFactorRoundingPolicy()
        if policy[-1] == ')':
            policy = policy[:-1]
        lastSep = policy.rfind("::")
        if lastSep != -1:
            policy = policy[:lastSep + 2]
        return policy

    def updateSystemInfo(self):
        """
        str = (f"<html><head/><body><h3>Build</h3><p> {QLibraryInfo.build()}</p>" +
               f"<h3>Operating System</h3><p> {QSysInfo().prettyProductName()}</p>" +
               f"<h3>Screens</h3><p>High DPI scale factor rounding policy:{WidgetGallery.highDpiScaleFactorRoundingPolicy()}</p><ol>")
        for screen in QGuiApplication.screens():
            current: bool = (screen == self.screen())
            str = "<li>"
            if (current):
                str += "<i>"
            str += f"{screen.name()}\{screen.geometry()}, {screen.logicalDotsPerInchX()} DPI, DPR={screen.devicePixelRatio()}"
            if (current):
                str += "</i>"
            str += "</li>"
        str += "</ol></body></html>"
        self.systemInfoTextBrowser.setHtml(str)
        """
        pass


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = ChocolafApp(sys.argv)
    # app.setStyle("Fusion")

    w = WidgetGallery()
    # w.setStyleSheet(app.getStyleSheet("Chocolaf"))
    w.move(20, 20)
    w.show()

    # rect = w.geometry()
    # w1 = WidgetGallery()
    # # w1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    # w1.move(rect.left() + rect.width() + 50,
    #         rect.top() + rect.height() // 4 + 50)
    # w1.show()

    return app.exec()


if __name__ == "__main__":
    main()
