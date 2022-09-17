# This Python file uses the following encoding: utf-8
import sys, os, pathlib
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# to detect dark themes (@see: https://pypi.org/project/darkdetect/)
import darkdetect

sys.path.append(os.path.join(pathlib.Path(__file__).parents[1], 'common'))
import mypyqt5_utils as utils

def main():
  app = QApplication(sys.argv)
  app.setStyle("Fusion")

  if darkdetect.isDark():
      utils.setDarkPalette(app)

  # let's check some QLocale stuff
  en_in = QLocale(QLocale.English, QLocale.India)
  curr = 1225245.78  # should format as 12,15,245.78
  print(f"{curr} in indian notation is {en_in.toCurrencyString(curr)}")

  mainWindow = QMainWindow()
  mainWindow.setWindowTitle("Step01 - Scribble Tutorial with PyQt5")
  mainWindow.resize(640, 480)
  mainWindow.setFont(QApplication.font("QMenu"))
  label = QLabel(f"{curr} in indian notation is {en_in.toCurrencyString(curr)}")
  mainWindow.setCentralWidget(label)
  mainWindow.show()
  return app.exec_()

if __name__ == "__main__":
     main()
