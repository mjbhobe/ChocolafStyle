import sys

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import chocolaf

import qtawesome as qta


def main():
    # app = QApplication(sys.argv)
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("WindowsDark")

    # create main gui
    my_icon = qta.icon('msc.chevron-left')
    my_button = QPushButton(my_icon, 'Works?')
    my_button.clicked.connect(QApplication.instance().quit)
    my_button.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
