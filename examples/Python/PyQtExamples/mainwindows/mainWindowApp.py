"""
* mainWindowApp.py: illustrates using QMainWindow class with Chocolaf
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
import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# sys.path.append(os.path.join(pathlib.Path(__file__).absolute().parents[2], 'common_files'))
# from pyqt5_utils import ChocolafApp
import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp
import textEditor_rc

MOD_PATH = os.path.abspath(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.curFile = ''

        self.textEdit = QPlainTextEdit()
        self.editorFont = QFont("Consolas", 11)
        self.textEdit.setFont(self.editorFont)
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

        self.readSettings()

        self.textEdit.document().contentsChanged.connect(self.documentWasModified)

        self.setCurrentFile('')
        self.setWindowIcon(QIcon(":/text_editor_icon.png"))

    def closeEvent(self, event):
        if self.maybeSave():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def newFile(self):
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFile('')

    def open(self):
        if self.maybeSave():
            docsPath = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open file', docsPath[-1],
                                                      "Text Files (*.txt *.c *.cpp *.h *.hxx *.py *.java *.bat *.sh)")
            # fileName, _ = QFileDialog.getOpenFileName(self)
            if fileName:
                self.loadFile(fileName)

    def save(self):
        if self.curFile:
            return self.saveFile(self.curFile)

        return self.saveAs()

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As...", MOD_PATH)
        if fileName:
            return self.saveFile(fileName)

        return False

    def about(self):
        QMessageBox.about(self, "About Application",
                          "The <b>Chocolaf-TextEditor</b> example demonstrates how to write "
                          "modern GUI applications using PyQt, with a menu bar, "
                          "toolbars, and a status bar.<br/><br/>"
                          "Author: Manish Bhobe<br/><br/>"
                          "<small>Code released for illustration purposes only!</small>")

    def documentWasModified(self):
        self.setWindowModified(self.textEdit.document().isModified())

    def createActions(self):
        root = QFileInfo(__file__).absolutePath()

        self.newAct = QAction(QIcon(':/file_new.png'), "&New", self,
                              shortcut=QKeySequence.New, statusTip="Create a new file",
                              triggered=self.newFile)

        self.openAct = QAction(QIcon(':/file_open.png'), "&Open...",
                               self, shortcut=QKeySequence.Open,
                               statusTip="Open an existing file", triggered=self.open)

        saveIcon = QIcon(':/file_save.png')
        saveIcon.addPixmap(QPixmap(":/file_save-1d.png"), QIcon.Disabled)
        self.saveAct = QAction(saveIcon, "&Save", self, shortcut=QKeySequence.Save,
                               statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QAction("Save &As...", self,
                                 shortcut=QKeySequence.SaveAs,
                                 statusTip="Save the document under a new name",
                                 triggered=self.saveAs)

        self.exitAct = QAction(QIcon(':/on-off.png'), "E&xit", self, shortcut="Ctrl+Q",
                               statusTip="Exit the application", triggered=self.close)

        cutIcon = QIcon(':/edit_cut.png')
        cutIcon.addPixmap(QPixmap(":/edit_cut-d.png"), QIcon.Disabled)
        self.cutAct = QAction(cutIcon, "Cu&t", self, shortcut=QKeySequence.Cut,
                              statusTip="Cut the current selection's contents to the clipboard",
                              triggered=self.textEdit.cut)

        copyIcon = QIcon(':/edit_copy.png')
        copyIcon.addPixmap(QPixmap(":/edit_copy-d.png"), QIcon.Disabled)
        self.copyAct = QAction(copyIcon, "&Copy", self, shortcut=QKeySequence.Copy,
                               statusTip="Copy the current selection's contents to the clipboard",
                               triggered=self.textEdit.copy)

        pasteIcon = QIcon(':/edit_paste.png')
        pasteIcon.addPixmap(QPixmap(":/edit_paste-d.png"), QIcon.Disabled)
        self.pasteAct = QAction(pasteIcon, "&Paste", self, shortcut=QKeySequence.Paste,
                                statusTip="Paste the clipboard's contents into the current selection",
                                triggered=self.textEdit.paste)

        self.wordWrapAct = QAction(QIcon(':/word_wrap.png'), "Word &wrap", self,
                                   statusTip="Toggle word wrapping in editor",
                                   triggered=self.enableDisableWordWrap)
        self.wordWrapAct.setCheckable(True)
        self.wordWrapAct.setChecked(True)

        self.fontAct = QAction(QIcon(':/font_size.png'), "Select Font...", self,
                               statusTip="Choose default font used by editor",
                               triggered=self.chooseFont)

        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                                  statusTip="Show the Qt library's About box",
                                  triggered=QApplication.instance().aboutQt)

        self.cutAct.setEnabled(False)
        self.copyAct.setEnabled(False)
        self.textEdit.copyAvailable.connect(self.cutAct.setEnabled)
        self.textEdit.copyAvailable.connect(self.copyAct.setEnabled)

    def createMenus(self):
        menuBar = self.menuBar()
        menuBar.setStyleSheet("QMenuBar {background-color: rgb(25, 32, 48);}")

        self.fileMenu = menuBar.addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = menuBar.addMenu("&Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.fileMenu.addSeparator()
        self.editMenu.addAction(self.wordWrapAct)
        self.editMenu.addAction(self.fontAct)

        menuBar.addSeparator()

        self.helpMenu = menuBar.addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)
        self.editToolBar.addAction(self.wordWrapAct)

    def createStatusBar(self):
        statusBar = self.statusBar()
        statusBar.setStyleSheet("QStatusBar {background-color: rgb(25, 32, 48);}")
        statusBar.showMessage("Ready")

    def readSettings(self):
        settings = QSettings("ChocoApps", "Chocolaf-TextEditor")
        pos = settings.value("pos", QPoint(200, 200))
        size = settings.value("size", QSize(400, 400))
        fontFamily = settings.value("fontFamily", "monospaced")
        fontSize = settings.value("fontSize", 11)
        self.editorFont = QFont(fontFamily, fontSize)
        self.textEdit.setFont(self.editorFont)
        _logger.info(f"Settings read: pos = {pos}, size = {size}, fontFamily = {fontFamily}, fontSize = {fontSize}")
        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        settings = QSettings("ChocoApps", "Chocolaf-TextEditor")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())
        settings.setValue("fontFamily", self.editorFont.family())
        settings.setValue("fontSize", self.editorFont.pointSize())
        _logger.info(
            f"Settings written: pos = {self.pos()}, size = {self.size()}, fontFamily = {self.editorFont.family()}, fontSize = {self.editorFont.pointSize()}")

    def maybeSave(self):
        if self.textEdit.document().isModified():
            ret = QMessageBox.warning(self, "Application",
                                      "The document has been modified.\nDo you want to save "
                                      "your changes?",
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if ret == QMessageBox.Save:
                return self.save()

            if ret == QMessageBox.Cancel:
                return False

        return True

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        inf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.textEdit.setPlainText(inf.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outf << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File saved", 2000)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.textEdit.document().setModified(False)
        self.setWindowModified(False)

        if self.curFile:
            shownName = self.strippedName(self.curFile)
        else:
            shownName = 'untitled.txt'

        self.setWindowTitle("%s[*] - PyQtTextEditor" % shownName)

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()

    def enableDisableWordWrap(self):
        if self.wordWrapAct.isChecked():
            self.textEdit.setLineWrapMode(QTextEdit.WidgetWidth)
        else:
            self.textEdit.setLineWrapMode(QTextEdit.NoWrap)

    def chooseFont(self):
        fontDialog = QFontDialog(self)
        fontDialog.setCurrentFont(self.editorFont)
        # display only scalable monospaced fonts
        fontDialog.setOption(QFontDialog.ScalableFonts, False)
        fontDialog.setOption(QFontDialog.NonScalableFonts, False)
        fontDialog.setOption(QFontDialog.MonospacedFonts, True)
        fontDialog.setOption(QFontDialog.ProportionalFonts, False)

        editorFont, ok = fontDialog.getFont()
        if ok:
            self.textEdit.setFont(editorFont)


if __name__ == '__main__':
    LOG_FILE_PATH = f"{__file__}.log"
    logging.basicConfig(filename=LOG_FILE_PATH, level=logging.DEBUG)
    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
