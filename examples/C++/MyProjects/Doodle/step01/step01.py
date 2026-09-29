# This Python file uses the following encoding: utf-8
import sys, os, pathlib
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *

sys.path.append(os.path.join(pathlib.Path(__file__).parents[1], 'common'))
import mypyqt_utils as utils

def main():
  app = QApplication(sys.argv)

  en_us = QLocale("en_US")
  en_in = QLocale(QLocale.English, QLocale.India)
  curr = 1225245.78  # should format as 12,15,245.78
  usd_to_inr = 96.543
  label_str: str = f"{en_us.toCurrencyString(curr)} is {en_in.toCurrencyString(curr * usd_to_inr)} @ 1 USD = {usd_to_inr} INR"

  mainWindow = QMainWindow()
  mainWindow.setWindowTitle(f"Step01 - Scribble Tutorial with PyQt{PYQT_VERSION_STR}")
  mainWindow.resize(640, 480)
  menuFont : QFont = QApplication.font("QMenu")
  menuFont.setPointSize(14)
  mainWindow.setFont(menuFont)

  label = QLabel(label_str)
  label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
  mainWindow.setCentralWidget(label)
  mainWindow.show()

  return app.exec_()

if __name__ == "__main__":
     main()
