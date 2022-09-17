"""
* tabDemo.py - demonstrated tab controls
* @author: Manish Bhobe
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import chocolaf
from chocolaf.utils.chocolafapp import ChocolafApp


class TabDemoWidget(QTabWidget):
    def __init__(self, parent=None):
        super(TabDemoWidget, self).__init__(parent)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.setWindowTitle("tab demo")

    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow("Name", QLineEdit())
        layout.addRow("Address", QLineEdit())
        self.setTabText(0, "Contact Details")
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"), sex)
        layout.addRow("Date of Birth", QLineEdit())
        self.setTabText(1, "Personal Details")
        self.tab2.setLayout(layout)

    def tab3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("subjects"))
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))
        self.setTabText(2, "Education Details")
        self.tab3.setLayout(layout)


class TabDemoWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super(TabDemoWindow, self).__init__(parent)
        layout = QVBoxLayout()
        widget = TabDemoWidget(self)
        layout.addWidget(widget)
        self.setLayout(layout)
        self.setWindowTitle("QTabWidget Demo")
        self.resize(640, 200)


def main():
    app = ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")
    ex = TabDemoWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
