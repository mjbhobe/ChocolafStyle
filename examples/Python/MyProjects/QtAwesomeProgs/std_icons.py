import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import chocolaf


def main():
    # app = QApplication(sys.argv)
    app = chocolaf.ChocolafApp(sys.argv)
    # app.setStyle("WindowsDark")
    app.setStyle("Fusion")
    stylesheet = """
        QPushButton {
            min-height: 1.5em;
        }
    # """
    # app.setStyleSheet(stylesheet)

    icon_names = chocolaf.get_icon_names()
    print(icon_names)
    col_count = 7
    row_count = len(icon_names) // col_count
    if len(icon_names) % row_count > 0:
        row_count += 1

    win: QWidget = QWidget()
    layout: QGridLayout = QGridLayout()
    for row in range(row_count):
        for col in range(col_count):
            index = row * col_count + col
            if index >= len(icon_names):
                break
            icon = chocolaf.get_icon(icon_names[index])
            button = QPushButton(icon, icon_names[index])
            button.setStyleSheet(stylesheet)
            layout.addWidget(button, row, col)
    win.setLayout(layout)
    win.setWindowTitle("Chocolaf Icons Cache")
    win.move(QPoint(100, 100))
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
