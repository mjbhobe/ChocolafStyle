#!/usr/bin/env python
"""
* memoryusage.py - pie chart showing memory usage on your system
* @author (Chocolaf): Manish Bhobe
*
* PyQt demo code taken from https://github.com/baoboa/pyqt5/tree/master/examples/widgets
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import os
import pathlib
import sys
import unicodedata

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *

# sys.path.append(os.path.join(pathlib.Path(__file__).absolute().parents[2], 'common_files'))
# from pyqt5_utils import ChocolafApp
from chocolaf.palettes import ChocolafPalette
from chocolaf.utils.chocolafapp import ChocolafApp


def run_process(command, args):
    process = QProcess()
    process.start(command, args)
    process.waitForFinished()
    std_output = process.readAllStandardOutput().data().decode("utf-8")
    return std_output.split("\n")


def getMemoryUsage():
    result = []

    if sys.platform == "win32":
        # Windows platform
        for line in run_process('tasklist', [])[3:]:
            if len(line) >= 74:
                command = line[0:23].strip()
                if command.endswith(".exe"):
                    command = command[0:len(command) - 4]
                memory_usage = float(
                    line[64:74].strip().replace(',', '').replace('.', ''))
                legend = ''
                if memory_usage > 10240:
                    mb = memory_usage / 1024
                    legend = f'{command} {mb}M'
                else:
                    legend = f'{command} {memory_usage}K'
                result.append([legend, memory_usage])
    else:
        # for Mac & *nix based platforms
        """
        Sample output of the ps -ev command on Linux is
        PID TTY      STAT   TIME  MAJFL   TRS   DRS   RSS %MEM COMMAND
      37144 pts/1    Ss     0:00     20   697  7526  3516  0.0 /bin/bash COLORFGBG=15;0 COLORTERM=truecolor DBUS_SESSION
      45285 pts/1    S      0:00      0   697  7090  2116  0.0 /bin/bash /usr/bin/atom . SHELL=/bin/bash SESSION_MANAGER
      45287 pts/1    Sl     0:45     87 100894 5171701 255372  3.1 /usr/lib/electron11/electron --executed-from=/home/mj
      45290 pts/1    S      0:00      0 100894 358069 81684  1.0 /usr/lib/electron11/electron --type=zygote --no-zygote-
      45291 pts/1    S      0:00      0 100894 358069 81576  1.0 /usr/lib/electron11/electron --type=zygote
      45293 pts/1    S      0:00      0 100894 358069 13196  0.1 /usr/lib/electron11/electron --type=zygote
        """
        ps_options = ['-e', '-v'] if sys.platform == 'darwin' else ['-e', 'v']
        memory_column = 11 if sys.platform == 'darwin' else 8
        command_column = 12 if sys.platform == 'darwin' else 9
        for line in run_process('ps', ps_options):
            tokens = line.split(None)
            if len(tokens) > command_column and "PID" not in tokens:
                command = tokens[command_column]
                if not command.startswith('['):
                    command = os.path.basename(command)
                    memory_usage = round(
                        float(tokens[memory_column].replace(',', '.')))
                    legend = f'{command} {memory_usage}%'
                    result.append([legend, memory_usage])

    result.sort(key=lambda x: x[1], reverse=True)
    return result


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Memory Usage')

        memory_usage = getMemoryUsage()
        if len(memory_usage) > 5:
            # pick top 5 only!
            memory_usage = memory_usage[0:4]

        self.series = QPieSeries()
        for item in memory_usage:
            self.series.append(item[0], item[1])

        chart_slice = self.series.slices()[0]
        chart_slice.setExploded()
        chart_slice.setLabelVisible()
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self._chart_view = QChartView(self.chart)
        self.setCentralWidget(self._chart_view)


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")
    main_win = MainWindow()
    available_geometry = main_win.screen().availableGeometry()
    size = available_geometry.height() * 3 / 4
    main_win.resize(size, size)
    main_win.show()
    sys.exit(app.exec())
