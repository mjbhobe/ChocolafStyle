import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QSyntaxHighlighter,
    QTextEdit,
    QAction,
    QFileDialog,
    QMenu,
    QStatusBar,
    QToolBar,
)
from PyQt6.QtGui import QTextCharFormat, QFont, QColor, QTextCursor


class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Python code"""

    def __init__(self, parent):
        super().__init__(parent)

        # Keywords
        keywords = [
            "and",
            "as",
            "assert",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "nonlocal",
            "not",
            "or",
            "pass",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield",
        ]
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#008000"))
        keyword_format.setFontWeight(QFont.Bold)
        for keyword in keywords:
            self.highlightFor(keyword, keyword_format)

        # Operators
        operators = [
            "==",
            "!=",
            "<",
            ">",
            "<=",
            ">=",
            "+",
            "-",
            "*",
            "/",
            "//",
            "%",
            "=",
            "+=",
            "-=",
            "*=",
            "/=",
            "%=",
            "@",
            "&",
            "|",
            "^",
            "~",
            ">>",
            "<<",
        ]
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor("#9932CC"))
        for operator in operators:
            self.highlightFor(operator, operator_format)

        # Delimiters
        delimiters = [
            "{",
            "}",
            "(",
            ")",
            "[",
            "]",
            ";",
            ":",
            ",",
            ".",
            "...",
        ]
        delimiter_format = QTextCharFormat()
        delimiter_format.setForeground(QColor("#666666"))
        for delimiter in delimiters:
            self.highlightFor(delimiter, delimiter_format)

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#AA87FF"))
        self.highlightFor(r"'[^']*'", string_format)
        self.highlightFor(r'"[^"]*"', string_format)

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#808080"))
        self.highlightFor(r"#.*", comment_format)


class CodeEditor(QTextEdit):
    """Python code editor with additional features"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Syntax highlighting
        self.highlighter = PythonHighlighter(self)

        # Smart auto indentation
        self.setTabStopWidth(4)
        self.setIndentationWidth(4)
        self.setAutoFillBackground(True)

        # Cursor position update
        self.cursorPositionChanged.connect(self.update_status_bar)

    def update_status_bar(self):
        """Update status bar with cursor position"""
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.statusBar().showMessage(f"Line: {line}, Column: {column}")


class MainWindow(QtWidgets.QMainWindow):
    """Main window of the application"""

    def __init__(self):
        super().__init__()

        # Initialize UI elements
        self.code_editor = CodeEditor()
        self.status_bar = QStatusBar()

        # Create menu bar
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        self.edit_menu = self.menu_bar.addMenu("Edit")

        # Create actions
        self.new_file_action = QAction(
            "New", self, shortcut="Ctrl+N", triggered=self.new_file
        )
        self.open_file_action = QAction(
            "Open...", self, shortcut="Ctrl+O", triggered=self.open_file
        )
        self.save_file_action = QAction(
            "Save", self, shortcut="Ctrl+S", triggered=self.save_file
        )
        # self.save_as_action = QAction("Save As...",
