# hello.py: signals & slots
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# using qdarkstyle (@see: https://github.com/ColinDuquesnoy/QDarkStyleSheet)
import qdarkstyle
# to detect dark themes (@see: https://pypi.org/project/darkdetect/)
import darkdetect

MIN_C, MAX_C = -100, 100

app = QApplication(sys.argv)
app.setStyle('Fusion')
# font = QFont("SF UI Text", 11)
app.setFont(QApplication.font("QMenu"))
if darkdetect.isDark():
    # apply dark stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
print(f"Available styles {QStyleFactory.keys()}")
widget = QWidget()
widget.setWindowTitle("Hello")
layout = QVBoxLayout()
label = QLabel(f"Welcome to PyQt {PYQT_VERSION_STR} GUI programming!")
layout.addWidget(label)
widget.setLayout(layout)
widget.show()

sys.exit(app.exec_())
