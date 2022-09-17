"""
* labels.py: Using QLabel class - illustrates various styles of QLabels
*   using both Chocolaf style and QDarkStyle-dark stylesheets
* @author: Manish Bhobe
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import os
import pathlib
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from chocolaf.utils.chocolafapp import ChocolafApp


class Window(QWidget):
    def __init__(self, parent: QWidget = None):
        super(Window, self).__init__(parent)

        groupBox = QGroupBox("QLabels")

        label1 = QLabel("Left aligned")
        # left alignment is default, so following call is optional
        # label1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label2 = QLabel("Right aligned")
        label2.setAlignment(Qt.AlignmentFlag.AlignRight)
        label3 = QLabel("Center Aligned")
        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label4 = QLabel("Disabled QLabel")
        label4.setEnabled(False)
        label5 = QLabel("Microsoft.com")
        label5.setOpenExternalLinks(True)
        label5.linkActivated.connect(self.clicked)
        # label with a picture (pixmap)
        label6 = QLabel()
        pixmap = QPixmap()
        # relative paths may not always work, so derive complete path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(dir_path, "images", "python.png")
        pixmap.load(image_path)
        label6.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(label4)
        layout.addWidget(label5)
        layout.addWidget(label6)
        groupBox.setLayout(layout)

        mainLayout = QGridLayout()
        mainLayout.addWidget(groupBox, 0, 0)
        self.setLayout(mainLayout)
        self.setWindowTitle("QLabel Demo")

    def clicked(self):
        print("You clicked the microsoft.com link")


"""
def loadStyleSheet() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    print(f"loadStyleSheet() -> You are {here}")
    darkss_dir = os.path.join(here, "styles", "dark")
    sys.path.append(darkss_dir)
    import stylesheet_rc

    darkss_path = os.path.join(darkss_dir, "stylesheet.css")
    assert os.path.exists(darkss_path)
    print(f"LoadStyleSheet() -> loading dark stylesheet from {darkss_path}")
    stylesheet = ""
    with open(darkss_path, "r") as f:
        stylesheet = f.read()
    return stylesheet
"""


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = ChocolafApp(sys.argv)
    print(f"Available styles: {app.availableStyles()}")

    win = Window()
    win.setStyleSheet(app.getStyleSheet("Chocolaf"))
    win.move(50, 50)
    win.setWindowTitle("Chocolaf Stylesheet")
    win.show()

    rect = win.geometry()
    win1 = Window()
    win1.setStyleSheet(app.getStyleSheet("QDarkStyle-dark"))
    win1.setWindowTitle("QDarkStyle-dark stylesheet")
    win1.move(rect.left() + rect.width() + 20, rect.top())
    win1.show()

    return app.exec()


if __name__ == "__main__":
    main()
