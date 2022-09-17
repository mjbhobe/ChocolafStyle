"""
* spreadsheetitem.py 
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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from util import decode_pos


class SpreadSheetItem(QTableWidgetItem):

    def __init__(self, text=None):
        if text is not None:
            super(SpreadSheetItem, self).__init__(text)
        else:
            super(SpreadSheetItem, self).__init__()

        self.isResolving = False

    def clone(self):
        item = super(SpreadSheetItem, self).clone()
        item.isResolving = self.isResolving

        return item

    def formula(self):
        return super(SpreadSheetItem, self).data(Qt.DisplayRole)

    def data(self, role):
        if role in (Qt.EditRole, Qt.StatusTipRole):
            return self.formula()
        if role == Qt.DisplayRole:
            return self.display()
        t = str(self.display())
        try:
            number = int(t)
        except ValueError:
            number = None
        if role == Qt.TextColorRole:
            if number is None:
                return QColor(Qt.black)
            elif number < 0:
                return QColor(Qt.red)
            return QColor(Qt.blue)

        if role == Qt.TextAlignmentRole:
            if t and (t[0].isdigit() or t[0] == '-'):
                return Qt.AlignRight | Qt.AlignVCenter
        return super(SpreadSheetItem, self).data(role)

    def setData(self, role, value):
        super(SpreadSheetItem, self).setData(role, value)
        if self.tableWidget():
            self.tableWidget().viewport().update()

    def display(self):
        # avoid circular dependencies
        if self.isResolving:
            return None
        self.isResolving = True
        result = self.computeFormula(self.formula(), self.tableWidget())
        self.isResolving = False
        return result

    def computeFormula(self, formula, widget):
        if formula is None:
            return None
        # check if the string is actually a formula or not
        slist = formula.split(' ')
        if not slist or not widget:
            # it is a normal string
            return formula
        op = slist[0].lower()
        firstRow = -1
        firstCol = -1
        secondRow = -1
        secondCol = -1
        if len(slist) > 1:
            firstRow, firstCol = decode_pos(slist[1])
        if len(slist) > 2:
            secondRow, secondCol = decode_pos(slist[2])
        start = widget.item(firstRow, firstCol)
        end = widget.item(secondRow, secondCol)
        firstVal = 0
        try:
            firstVal = start and int(start.text()) or 0
        except ValueError:
            pass
        secondVal = 0
        try:
            secondVal = end and int(end.text()) or 0
        except ValueError:
            pass
        result = None
        if op == "sum":
            sum_ = 0
            for r in range(firstRow, secondRow + 1):
                for c in range(firstCol, secondCol + 1):
                    tableItem = widget.item(r, c)
                    if tableItem and tableItem != self:
                        try:
                            sum_ += int(tableItem.text())
                        except ValueError:
                            pass
            result = sum_
        elif op == "+":
            result = (firstVal + secondVal)
        elif op == "-":
            result = (firstVal - secondVal)
        elif op == "*":
            result = (firstVal * secondVal)
        elif op == "/":
            if secondVal == 0:
                result = "nan"
            else:
                result = (firstVal / secondVal)
        elif op == "=":
            if start:
                result = start.text()
        else:
            result = formula
        return result
