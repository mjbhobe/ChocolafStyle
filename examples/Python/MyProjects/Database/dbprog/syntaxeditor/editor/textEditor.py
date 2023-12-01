from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class TextEditor(QTextEdit):
    """base multi-line text editor with initial settings & auto-indent ability"""

    def __init__(self):
        super(QTextEdit, self).__init__()
        self.editor_font = QFont(
            "The Sans Mono-, SF Mono, Consolas, Monospace",
            10,
        )
        self.setFont(self.editor_font)
        # self tabstops to 4 spaces
        self.tabstops = 4
        self.autoindent = True
        font = self.font()
        fontMetrics = QFontMetrics(font)
        spaceWidth = fontMetrics.averageCharWidth()
        # lineHeight = fontMetrics.lineSpacing() * 1.5
        self.setTabStopDistance(spaceWidth * 4)
        # set line spacing to 1.5 times
        self.setStyleSheet("line-height: 150%;")
        self.setMinimumSize(100, 100)

    def auto_indent(self):
        current_line = self.textCursor().block().text()

        i, indentation = (0, 0)
        spacesText = ""
        if current_line != "":
            while current_line[i].isspace():
                indentation += 1 if current_line[i] == " " else 0
                indentation += self.tabstops if current_line[i] == "\t" else 0
                spacesText += current_line[i]
                i += 1
        self.insertPlainText(f"\n{spacesText}")
        # move the cursor by indentation
        # cursor.movePosition(
        #     QTextCursor.MoveOperation.Right,
        #     QTextCursor.MoveMode.MoveAnchor,
        #     indentation,
        # )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            if self.autoindent:
                self.auto_indent()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)
