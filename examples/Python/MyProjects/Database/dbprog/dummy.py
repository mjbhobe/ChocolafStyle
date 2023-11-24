import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class AutoIndent(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor_font = QFont("Monospace", 10)
        self.setFont(self.editor_font)
        self.tabstops = 4
        font = self.font()
        fontMetrics = QFontMetrics(font)
        spaceWidth = fontMetrics.averageCharWidth()
        self.setTabStopDistance(spaceWidth * 4)
        self.setStyleSheet("line-height: 150%;")

        self.current_line = 0
        self.previous_line = ""

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.auto_indent()
        else:
            super().keyPressEvent(event)

    def auto_indent(self):
        current_line = self.textCursor().block().text()

        i, indentation = (0, 0)
        if current_line != "":
            while current_line[i].isspace():
                indentation += 1 if current_line[i] == " " else 0
                indentation += self.tabstops if current_line[i] == "\t" else 0
                i += 1
            spaces = " " * indentation
            self.insertPlainText(f"\n{spaces}")

        # previous_line = self.document().findBlockByNumber(self.current_line - 1).text()

        # if current_line.startswith(" "):
        #     current_line = current_line[1:]

        # if previous_line.endswith(":"):
        #     self.insertPlainText("    " + current_line)
        # else:
        #     self.insertPlainText(f"\n{current_line}")

        # self.current_line += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setCentralWidget(AutoIndent())
    window.show()

    sys.exit(app.exec())
