"""
* spreadsheet.py - rhudementary spreadsheet using PyQt and Chocolaf
* @author (Chocolaf): Manish Bhobe
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!
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
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *

import chocolaf
from printview import PrintView
from spreadsheetdelegate import SpreadSheetDelegate
from spreadsheetitem import SpreadSheetItem
from util import decode_pos, encode_pos

import spreadsheet_rc


class SpreadSheet(QMainWindow):
    dateFormats = ["dd/MM/yyyy", "yyyy/M/dd", "dd.MM.yyyy"]

    currentDateFormat = dateFormats[0]

    def __init__(self, rows, cols, parent=None):
        super(SpreadSheet, self).__init__(parent)

        self.toolBar = QToolBar()
        self.addToolBar(self.toolBar)
        self.formulaInput = QLineEdit()
        self.cellLabel = QLabel(self.toolBar)
        self.cellLabel.setMinimumSize(80, 0)
        self.toolBar.addWidget(self.cellLabel)
        self.toolBar.addWidget(self.formulaInput)
        self.table = QTableWidget(rows, cols, self)
        for c in range(cols):
            character = chr(ord("A") + c)
            self.table.setHorizontalHeaderItem(c, QTableWidgetItem(character))

        self.table.setItemPrototype(self.table.item(rows - 1, cols - 1))
        self.table.setItemDelegate(SpreadSheetDelegate(self))
        self.createActions()
        self.updateColor(0)
        self.setupMenuBar()
        self.setupContents()
        self.setupContextMenu()
        self.setCentralWidget(self.table)
        self.statusBar()
        self.table.currentItemChanged.connect(self.updateStatus)
        self.table.currentItemChanged.connect(self.updateColor)
        self.table.currentItemChanged.connect(self.updateLineEdit)
        self.table.itemChanged.connect(self.updateStatus)
        self.formulaInput.returnPressed.connect(self.returnPressed)
        self.table.itemChanged.connect(self.updateLineEdit)
        self.setWindowTitle("Spreadsheet")

    def createActions(self):
        self.cell_sumAction = QAction("Sum", self)
        self.cell_sumAction.triggered.connect(self.actionSum)

        self.cell_addAction = QAction("&Add", self)
        self.cell_addAction.setShortcut(Qt.CTRL | Qt.Key_Plus)
        self.cell_addAction.triggered.connect(self.actionAdd)

        self.cell_subAction = QAction("&Subtract", self)
        self.cell_subAction.setShortcut(Qt.CTRL | Qt.Key_Minus)
        self.cell_subAction.triggered.connect(self.actionSubtract)

        self.cell_mulAction = QAction("&Multiply", self)
        self.cell_mulAction.setShortcut(Qt.CTRL | Qt.Key_multiply)
        self.cell_mulAction.triggered.connect(self.actionMultiply)

        self.cell_divAction = QAction("&Divide", self)
        self.cell_divAction.setShortcut(Qt.CTRL | Qt.Key_division)
        self.cell_divAction.triggered.connect(self.actionDivide)

        self.fontAction = QAction("Font...", self)
        self.fontAction.setShortcut(Qt.CTRL | Qt.Key_F)
        self.fontAction.triggered.connect(self.selectFont)

        self.colorAction = QAction(QIcon(QPixmap(16, 16)), "Background &Color...", self)
        self.colorAction.triggered.connect(self.selectColor)

        self.clearAction = QAction("Clear", self)
        self.clearAction.setShortcut(Qt.Key_Delete)
        self.clearAction.triggered.connect(self.clear)

        self.aboutSpreadSheet = QAction("About Spreadsheet", self)
        self.aboutSpreadSheet.triggered.connect(self.showAbout)

        self.exitAction = QAction("E&xit", self)
        self.exitAction.setShortcut(QKeySequence.Quit)
        self.exitAction.triggered.connect(QApplication.instance().quit)

        self.printAction = QAction("&Print", self)
        self.printAction.setShortcut(QKeySequence.Print)
        self.printAction.triggered.connect(self.print_)

        self.firstSeparator = QAction(self)
        self.firstSeparator.setSeparator(True)

        self.secondSeparator = QAction(self)
        self.secondSeparator.setSeparator(True)

    def setupMenuBar(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.dateFormatMenu = self.fileMenu.addMenu("&Date format")
        self.dateFormatGroup = QActionGroup(self)
        for f in self.dateFormats:
            action = QAction(f, self, checkable=True, triggered=self.changeDateFormat)
            self.dateFormatGroup.addAction(action)
            self.dateFormatMenu.addAction(action)
            if f == self.currentDateFormat:
                action.setChecked(True)

        self.fileMenu.addAction(self.printAction)
        self.fileMenu.addAction(self.exitAction)
        self.cellMenu = self.menuBar().addMenu("&Cell")
        self.cellMenu.addAction(self.cell_addAction)
        self.cellMenu.addAction(self.cell_subAction)
        self.cellMenu.addAction(self.cell_mulAction)
        self.cellMenu.addAction(self.cell_divAction)
        self.cellMenu.addAction(self.cell_sumAction)
        self.cellMenu.addSeparator()
        self.cellMenu.addAction(self.colorAction)
        self.cellMenu.addAction(self.fontAction)
        self.menuBar().addSeparator()
        self.aboutMenu = self.menuBar().addMenu("&Help")
        self.aboutMenu.addAction(self.aboutSpreadSheet)

    def changeDateFormat(self):
        action = self.sender()
        oldFormat = self.currentDateFormat
        newFormat = self.currentDateFormat = action.text()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            date = QDate.fromString(item.text(), oldFormat)
            item.setText(date.toString(newFormat))

    def updateStatus(self, item):
        if item and item == self.table.currentItem():
            self.statusBar().showMessage(item.data(Qt.StatusTipRole), 1000)
            self.cellLabel.setText(
                "Cell: (%s)" % encode_pos(self.table.row(item), self.table.column(item))
            )

    def updateColor(self, item):
        pixmap = QPixmap(16, 16)
        color = QColor()
        if item:
            color = item.backgroundColor()
        if not color.isValid():
            color = self.palette().base().color()
        painter = QPainter(pixmap)
        painter.fillRect(0, 0, 16, 16, color)
        lighter = color.lighter()
        painter.setPen(lighter)
        # light frame
        painter.drawPolyline(QPoint(0, 15), QPoint(0, 0), QPoint(15, 0))
        painter.setPen(color.darker())
        # dark frame
        painter.drawPolyline(QPoint(1, 15), QPoint(15, 15), QPoint(15, 1))
        painter.end()
        self.colorAction.setIcon(QIcon(pixmap))

    def updateLineEdit(self, item):
        if item != self.table.currentItem():
            return
        if item:
            self.formulaInput.setText(item.data(Qt.EditRole))
        else:
            self.formulaInput.clear()

    def returnPressed(self):
        text = self.formulaInput.text()
        row = self.table.currentRow()
        col = self.table.currentColumn()
        item = self.table.item(row, col)
        if not item:
            self.table.setItem(row, col, SpreadSheetItem(text))
        else:
            item.setData(Qt.EditRole, text)
        self.table.viewport().update()

    def selectColor(self):
        item = self.table.currentItem()
        color = (
            item and QColor(item.background()) or self.table.palette().base().color()
        )
        color = QColorDialog.getColor(color, self)
        if not color.isValid():
            return
        selected = self.table.selectedItems()
        if not selected:
            return
        for i in selected:
            i and i.setBackground(color)
        self.updateColor(self.table.currentItem())

    def selectFont(self):
        selected = self.table.selectedItems()
        if not selected:
            return
        font, ok = QFontDialog.getFont(self.font(), self)
        if not ok:
            return
        for i in selected:
            i and i.setFont(font)

    def runInputDialog(
        self, title, c1Text, c2Text, opText, outText, cell1, cell2, outCell
    ):
        rows = []
        cols = []
        for r in range(self.table.rowCount()):
            rows.append(str(r + 1))
        for c in range(self.table.columnCount()):
            cols.append(chr(ord("A") + c))
        addDialog = QDialog(self)
        addDialog.setWindowTitle(title)
        group = QGroupBox(title, addDialog)
        group.setMinimumSize(250, 100)
        cell1Label = QLabel(c1Text, group)
        cell1RowInput = QComboBox(group)
        c1Row, c1Col = decode_pos(cell1)
        cell1RowInput.addItems(rows)
        cell1RowInput.setCurrentIndex(c1Row)
        cell1ColInput = QComboBox(group)
        cell1ColInput.addItems(cols)
        cell1ColInput.setCurrentIndex(c1Col)
        operatorLabel = QLabel(opText, group)
        operatorLabel.setAlignment(Qt.AlignHCenter)
        cell2Label = QLabel(c2Text, group)
        cell2RowInput = QComboBox(group)
        c2Row, c2Col = decode_pos(cell2)
        cell2RowInput.addItems(rows)
        cell2RowInput.setCurrentIndex(c2Row)
        cell2ColInput = QComboBox(group)
        cell2ColInput.addItems(cols)
        cell2ColInput.setCurrentIndex(c2Col)
        equalsLabel = QLabel("=", group)
        equalsLabel.setAlignment(Qt.AlignHCenter)
        outLabel = QLabel(outText, group)
        outRowInput = QComboBox(group)
        outRow, outCol = decode_pos(outCell)
        outRowInput.addItems(rows)
        outRowInput.setCurrentIndex(outRow)
        outColInput = QComboBox(group)
        outColInput.addItems(cols)
        outColInput.setCurrentIndex(outCol)

        cancelButton = QPushButton("Cancel", addDialog)
        cancelButton.clicked.connect(addDialog.reject)
        okButton = QPushButton("OK", addDialog)
        okButton.setDefault(True)
        okButton.clicked.connect(addDialog.accept)
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(okButton)
        buttonsLayout.addSpacing(10)
        buttonsLayout.addWidget(cancelButton)

        dialogLayout = QVBoxLayout(addDialog)
        dialogLayout.addWidget(group)
        dialogLayout.addStretch(1)
        dialogLayout.addItem(buttonsLayout)

        cell1Layout = QHBoxLayout()
        cell1Layout.addWidget(cell1Label)
        cell1Layout.addSpacing(10)
        cell1Layout.addWidget(cell1ColInput)
        cell1Layout.addSpacing(10)
        cell1Layout.addWidget(cell1RowInput)

        cell2Layout = QHBoxLayout()
        cell2Layout.addWidget(cell2Label)
        cell2Layout.addSpacing(10)
        cell2Layout.addWidget(cell2ColInput)
        cell2Layout.addSpacing(10)
        cell2Layout.addWidget(cell2RowInput)
        outLayout = QHBoxLayout()
        outLayout.addWidget(outLabel)
        outLayout.addSpacing(10)
        outLayout.addWidget(outColInput)
        outLayout.addSpacing(10)
        outLayout.addWidget(outRowInput)
        vLayout = QVBoxLayout(group)
        vLayout.addItem(cell1Layout)
        vLayout.addWidget(operatorLabel)
        vLayout.addItem(cell2Layout)
        vLayout.addWidget(equalsLabel)
        vLayout.addStretch(1)
        vLayout.addItem(outLayout)
        if addDialog.exec_():
            cell1 = cell1ColInput.currentText() + cell1RowInput.currentText()
            cell2 = cell2ColInput.currentText() + cell2RowInput.currentText()
            outCell = outColInput.currentText() + outRowInput.currentText()
            return True, cell1, cell2, outCell

        return False, None, None, None

    def actionSum(self):
        row_first = 0
        row_last = 0
        row_cur = 0
        col_first = 0
        col_last = 0
        col_cur = 0
        selected = self.table.selectedItems()
        if selected:
            first = selected[0]
            last = selected[-1]
            row_first = self.table.row(first)
            row_last = self.table.row(last)
            col_first = self.table.column(first)
            col_last = self.table.column(last)

        current = self.table.currentItem()
        if current:
            row_cur = self.table.row(current)
            col_cur = self.table.column(current)

        cell1 = encode_pos(row_first, col_first)
        cell2 = encode_pos(row_last, col_last)
        out = encode_pos(row_cur, col_cur)
        ok, cell1, cell2, out = self.runInputDialog(
            "Sum cells",
            "First cell:",
            "Last cell:",
            "\N{GREEK CAPITAL LETTER SIGMA}",
            "Output to:",
            cell1,
            cell2,
            out,
        )
        if ok:
            row, col = decode_pos(out)
            self.table.item(row, col).setText("sum %s %s" % (cell1, cell2))

    def actionMath_helper(self, title, op):
        cell1 = "C1"
        cell2 = "C2"
        out = "C3"
        current = self.table.currentItem()
        if current:
            out = encode_pos(self.table.currentRow(), self.table.currentColumn())
        ok, cell1, cell2, out = self.runInputDialog(
            title, "Cell 1", "Cell 2", op, "Output to:", cell1, cell2, out
        )
        if ok:
            row, col = decode_pos(out)
            self.table.item(row, col).setText("%s %s %s" % (op, cell1, cell2))

    def actionAdd(self):
        self.actionMath_helper("Addition", "+")

    def actionSubtract(self):
        self.actionMath_helper("Subtraction", "-")

    def actionMultiply(self):
        self.actionMath_helper("Multiplication", "*")

    def actionDivide(self):
        self.actionMath_helper("Division", "/")

    def clear(self):
        for i in self.table.selectedItems():
            i.setText("")

    def setupContextMenu(self):
        self.addAction(self.cell_addAction)
        self.addAction(self.cell_subAction)
        self.addAction(self.cell_mulAction)
        self.addAction(self.cell_divAction)
        self.addAction(self.cell_sumAction)
        self.addAction(self.firstSeparator)
        self.addAction(self.colorAction)
        self.addAction(self.fontAction)
        self.addAction(self.secondSeparator)
        self.addAction(self.clearAction)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    def setupContents(self):
        titleBackground = QColor(Qt.lightGray)
        titleFont = self.table.font()
        titleFont.setBold(True)
        # column 0
        self.table.setItem(0, 0, SpreadSheetItem("Item"))
        self.table.item(0, 0).setBackground(titleBackground)
        self.table.item(0, 0).setToolTip("This column shows the purchased item/service")
        self.table.item(0, 0).setFont(titleFont)
        self.table.setItem(1, 0, SpreadSheetItem("AirportBus"))
        self.table.setItem(2, 0, SpreadSheetItem("Flight (Munich)"))
        self.table.setItem(3, 0, SpreadSheetItem("Lunch"))
        self.table.setItem(4, 0, SpreadSheetItem("Flight (LA)"))
        self.table.setItem(5, 0, SpreadSheetItem("Taxi"))
        self.table.setItem(6, 0, SpreadSheetItem("Dinner"))
        self.table.setItem(7, 0, SpreadSheetItem("Hotel"))
        self.table.setItem(8, 0, SpreadSheetItem("Flight (Oslo)"))
        self.table.setItem(9, 0, SpreadSheetItem("Total:"))
        self.table.item(9, 0).setFont(titleFont)
        self.table.item(9, 0).setBackground(Qt.lightGray)
        # column 1
        self.table.setItem(0, 1, SpreadSheetItem("Date"))
        self.table.item(0, 1).setBackground(titleBackground)
        self.table.item(0, 1).setToolTip(
            "This column shows the purchase date, double click to change"
        )
        self.table.item(0, 1).setFont(titleFont)
        self.table.setItem(1, 1, SpreadSheetItem("15/6/2006"))
        self.table.setItem(2, 1, SpreadSheetItem("15/6/2006"))
        self.table.setItem(3, 1, SpreadSheetItem("15/6/2006"))
        self.table.setItem(4, 1, SpreadSheetItem("21/5/2006"))
        self.table.setItem(5, 1, SpreadSheetItem("16/6/2006"))
        self.table.setItem(6, 1, SpreadSheetItem("16/6/2006"))
        self.table.setItem(7, 1, SpreadSheetItem("16/6/2006"))
        self.table.setItem(8, 1, SpreadSheetItem("18/6/2006"))
        self.table.setItem(9, 1, SpreadSheetItem())
        self.table.item(9, 1).setBackground(Qt.lightGray)
        # column 2
        self.table.setItem(0, 2, SpreadSheetItem("Price"))
        self.table.item(0, 2).setBackground(titleBackground)
        self.table.item(0, 2).setToolTip("This column shows the price of the purchase")
        self.table.item(0, 2).setFont(titleFont)
        self.table.setItem(1, 2, SpreadSheetItem("150"))
        self.table.setItem(2, 2, SpreadSheetItem("2350"))
        self.table.setItem(3, 2, SpreadSheetItem("-14"))
        self.table.setItem(4, 2, SpreadSheetItem("980"))
        self.table.setItem(5, 2, SpreadSheetItem("5"))
        self.table.setItem(6, 2, SpreadSheetItem("120"))
        self.table.setItem(7, 2, SpreadSheetItem("300"))
        self.table.setItem(8, 2, SpreadSheetItem("1240"))
        self.table.setItem(9, 2, SpreadSheetItem())
        self.table.item(9, 2).setBackground(Qt.lightGray)
        # column 3
        self.table.setItem(0, 3, SpreadSheetItem("Currency"))
        self.table.item(0, 3).setBackground(titleBackground)
        self.table.item(0, 3).setToolTip("This column shows the currency")
        self.table.item(0, 3).setFont(titleFont)
        self.table.setItem(1, 3, SpreadSheetItem("NOK"))
        self.table.setItem(2, 3, SpreadSheetItem("NOK"))
        self.table.setItem(3, 3, SpreadSheetItem("EUR"))
        self.table.setItem(4, 3, SpreadSheetItem("EUR"))
        self.table.setItem(5, 3, SpreadSheetItem("USD"))
        self.table.setItem(6, 3, SpreadSheetItem("USD"))
        self.table.setItem(7, 3, SpreadSheetItem("USD"))
        self.table.setItem(8, 3, SpreadSheetItem("USD"))
        self.table.setItem(9, 3, SpreadSheetItem())
        self.table.item(9, 3).setBackground(Qt.lightGray)
        # column 4
        self.table.setItem(0, 4, SpreadSheetItem("Ex. Rate"))
        self.table.item(0, 4).setBackground(titleBackground)
        self.table.item(0, 4).setToolTip("This column shows the exchange rate to NOK")
        self.table.item(0, 4).setFont(titleFont)
        self.table.setItem(1, 4, SpreadSheetItem("1"))
        self.table.setItem(2, 4, SpreadSheetItem("1"))
        self.table.setItem(3, 4, SpreadSheetItem("8"))
        self.table.setItem(4, 4, SpreadSheetItem("8"))
        self.table.setItem(5, 4, SpreadSheetItem("7"))
        self.table.setItem(6, 4, SpreadSheetItem("7"))
        self.table.setItem(7, 4, SpreadSheetItem("7"))
        self.table.setItem(8, 4, SpreadSheetItem("7"))
        self.table.setItem(9, 4, SpreadSheetItem())
        self.table.item(9, 4).setBackground(Qt.lightGray)
        # column 5
        self.table.setItem(0, 5, SpreadSheetItem("NOK"))
        self.table.item(0, 5).setBackground(titleBackground)
        self.table.item(0, 5).setToolTip("This column shows the expenses in NOK")
        self.table.item(0, 5).setFont(titleFont)
        self.table.setItem(1, 5, SpreadSheetItem("* C2 E2"))
        self.table.setItem(2, 5, SpreadSheetItem("* C3 E3"))
        self.table.setItem(3, 5, SpreadSheetItem("* C4 E4"))
        self.table.setItem(4, 5, SpreadSheetItem("* C5 E5"))
        self.table.setItem(5, 5, SpreadSheetItem("* C6 E6"))
        self.table.setItem(6, 5, SpreadSheetItem("* C7 E7"))
        self.table.setItem(7, 5, SpreadSheetItem("* C8 E8"))
        self.table.setItem(8, 5, SpreadSheetItem("* C9 E9"))
        self.table.setItem(9, 5, SpreadSheetItem("sum F2 F9"))
        self.table.item(9, 5).setBackground(Qt.lightGray)

    def showAbout(self):
        QMessageBox.about(
            self,
            "About Spreadsheet",
            """
            <HTML>
            <p><b>This demo shows use of <c>QTableWidget</c> with custom handling for
             individual cells.</b></p>
            <p>Using a customized table item we make it possible to have dynamic
             output in different cells. The content that is implemented for this
             particular demo is:
            <ul>
            <li>Adding two cells.</li>
            <li>Subtracting one cell from another.</li>
            <li>Multiplying two cells.</li>
            <li>Dividing one cell with another.</li>
            <li>Summing the contents of an arbitrary number of cells.</li>
            </HTML>
        """,
        )

    def print_(self):
        printer = QPrinter(QPrinter.ScreenResolution)
        dlg = QPrintPreviewDialog(printer)
        view = PrintView()
        view.setModel(self.table.model())
        dlg.paintRequested.connect(view.print_)
        dlg.exec_()


if __name__ == "__main__":
    chocolaf.enable_hi_dpi()
    # app = chocolaf.ChocolafApp(sys.argv)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    sheet = SpreadSheet(10, 6)
    sheet.setWindowIcon(QIcon(QPixmap(":/images/interview.png")))
    sheet.resize(640, 420)
    sheet.show()
    sys.exit(app.exec_())
