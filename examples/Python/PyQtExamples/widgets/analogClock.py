"""
* analogClock.py: PyQt5 version of the Qt widgets analog clock demo using Chocolaf theme
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


class AnalogClock(QWidget):
    def __init__(self, parent: QWidget = None):
        super(AnalogClock, self).__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.setWindowTitle("Analog Clock")
        self.resize(200, 200)
        self.pixMap = QPixmap(200, 200)
        self.pixMap.fill(QColor(Qt.transparent))
        self.update()
        self.timer.start(1000)

    def update(self):
        hourHand = [QPoint(7, 8), QPoint(-7, 8), QPoint(0, -40)]
        minuteHand = [QPoint(7, 8), QPoint(-7, 8), QPoint(0, -70)]

        hourColor = QColor(Qt.white)  # QColor(180, 142, 173)
        minuteColor = QColor(0, 235, 203, 115)
        side = min(self.width(), self.height())
        time = QTime.currentTime()

        painter = QPainter(self.pixMap)
        try:
            painter.begin(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.translate(self.width() // 2, self.height() // 2)
            painter.scale(side / 200.0, side / 200.0)

            # draw hour hand
            painter.setPen(Qt.NoPen)
            painter.setBrush(hourColor)
            painter.save()
            painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
            painter.drawConvexPolygon(*hourHand)
            painter.restore()

            # draw hour notches across analog clock face
            painter.setPen(hourColor)
            for i in range(12):
                painter.drawLine(88, 0, 96, 0)
                painter.rotate(30.0)

            # draw minute hand
            painter.setPen(Qt.NoPen)
            painter.setBrush(minuteColor)
            painter.save()
            painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
            painter.drawConvexPolygon(*minuteHand)
            painter.restore()

            # draw minute notches across clock face
            painter.setPen(minuteColor)

            for j in range(60):
                if j % 5 != 0:
                    painter.drawLine(92, 0, 96, 0)
                painter.rotate(6.0)
        finally:
            painter.end()
            self.repaint()

    def paintEvent(self, e: QPaintEvent) -> None:
        # print("in paintEvent", flush=True)
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixMap)


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    # app = ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")
    app = QApplication(sys.argv)
    app.setStyleSheet(chocolaf.loadStyleSheet())

    clock = AnalogClock()
    clock.move(100, 100)
    clock.show()

    # rect = clock.geometry()
    # clock1 = AnalogClock()
    # clock1.setStyle(app.loadStyleSheet("QDarkStyle-dark"))
    # clock1.move(rect.left() + rect.width() // 4 + 20, rect.top() + rect.height() + 10)
    # clock1.show()

    return app.exec()


if __name__ == "__main__":
    main()
