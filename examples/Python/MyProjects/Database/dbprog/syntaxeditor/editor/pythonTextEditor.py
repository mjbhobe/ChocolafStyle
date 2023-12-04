from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from .textEditor import TextEditor


class PythonTextEditor(TextEditor):
    """base multi-line text editor with initial settings & auto-indent ability"""

    def __init__(self):
        super(PythonTextEditor, self).__init__()

    def auto_indent(self):
        """auto & smart indent for special keywords such as def, if, else, while"""
        current_line = self.textCursor().block().text()

        i, indentation = (0, 0)
        spacesText = ""
        if current_line != "":
            while current_line[i].isspace():
                indentation += 1 if current_line[i] == " " else 0
                indentation += self.tabstops if current_line[i] == "\t" else 0
                spacesText += current_line[i]
                i += 1

        # if current_line begins with special keywords
        special_kwds = ["class", "def", "if", "else", "elif", "while", "with"]
        sep_pat = r"\b"
        rex = r"^("
        for kwd in special_kwds:
            rex += f"{sep_pat}{kwd}{sep_pat}|"
        if rex.endswith("|"):
            rex = rex[: len(rex) - 1]
        rex += r")\s"

        re = QRegularExpression(rex)
        if re.match(current_line.strip()).hasMatch():
            # add extra indent
            self.insertPlainText(f"\n\t{spacesText}")
        else:
            self.insertPlainText(f"\n{spacesText}")
