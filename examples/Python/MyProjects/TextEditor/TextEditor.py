#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* TextEditor.py - code editor using QScintilla
* @author (Chocolaf): Manish Bhobe
*
* This application relies on QScintilla text component
*  >> pip install QScintilla
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import os
import sys
import pathlib
from argparse import ArgumentParser
from configparser import ConfigParser

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.Qsci import *

import chocolaf
from chocolaf import ChocolafPalette

logger = chocolaf.get_logger(pathlib.Path(__file__))


class TextEditorWindow(QMainWindow):
    def __init__(self):
        super(TextEditorWindow, self).__init__()
        self._editor = QsciScintilla()
        self._lexer = None
        # self._layout = QVBoxLayout()
        self.setupUi()

    def setupUi(self):
        # self._layout.addWidget(self._editor)
        # self.setLayout(self._layout)
        # self.resize(QGuiApplication.primaryScreen().availableSize() * (4 / 5))
        self.resize(QSize(1024, 768))
        self.setupEditor()
        self.setupActions()
        self.setupMenu()

        self._editor.setAcceptDrops(False)
        self.setAcceptDrops(True)

        self.setCentralWidget(self._editor)

    def setupActions(self):
        # open image
        self.openAction = QAction("&Open...", self)
        self.openAction.setShortcut(QKeySequence.New)
        self.openAction.setIcon(chocolaf.get_icon("File_Open"))
        # self.openAction.setIcon(QIcon(":/open.png"))
        self.openAction.setStatusTip("Open a file")
        self.openAction.triggered.connect(self.open)

        # exit
        self.exitAction = QAction("E&xit", self)
        self.exitAction.setShortcut(QKeySequence("Ctrl+Q"))
        self.exitAction.setIcon(chocolaf.get_icon("File_Exit"))
        self.exitAction.setStatusTip("Exit the application")
        self.exitAction.triggered.connect(QApplication.instance().quit)

    def setupMenu(self):
        # file menu
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("text/uri-list"):
            e.acceptProposedAction()

    def dropEvent(self, e):
        urls = e.mimeData().urls()  # is a list
        if len(urls) == 0:
            return

        fileName = urls[0].toLocalFile()
        if os.path.exists(fileName):
            self.loadTextFile(fileName)

    def setupEditor(self):
        editorFontPointSize = chocolaf.pixelsToPoints(16)
        logger.info(f"Setting editor font size to {editorFontPointSize} points")
        editor_font_names = "The Sans Mono-"  # Consolas, SF Mono, Menlo, Monaco, DejaVu Sans Mono, Monospace"
        logger.info(f"Using {editorFontPointSize} point font for editor")
        self._editorFont = QFont(editor_font_names)
        self._editorFont.setPointSize(editorFontPointSize)
        self._editorFontBold = QFont(editor_font_names)
        self._editorFontBold.setPointSize(editorFontPointSize)
        self._editorFontBold.setBold(True)
        self._editorFontItalic = QFont(editor_font_names)
        self._editorFontItalic.setPointSize(editorFontPointSize)
        self._editorFontItalic.setItalic(True)
        # screenDpi = QApplication.desktop().logicalDpiX()
        # self._editorFont.setPointSize(int(12 / 72 * screenDpi))
        self._editor.setFont(self._editorFont)
        self._editor.setLexer(None)
        self._editor.setUtf8(True)
        self._editor.setTabWidth(4)
        self._editor.setIndentationsUseTabs(True)
        self._editor.setIndentationGuides(True)
        self._editor.setAutoIndent(True)
        self._editor.setCaretForegroundColor(ChocolafPalette.Text_Color)
        self._editor.setCaretWidth(3)
        # set current line background color
        self._editor.setCaretLineVisible(True)
        self._editor.setCaretLineBackgroundColor(QColor("#484848"))
        # setup margins
        self._editor.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self._editor.setMarginType(1, QsciScintilla.MarginType.TextMargin)
        self._editor.setMarginWidth(0, "99999")
        self._editor.setMarginWidth(1, "99")
        self._editor.setMarginsBackgroundColor(ChocolafPalette.Button_Color)
        self._editor.setMarginsForegroundColor(ChocolafPalette.Text_Color)

    def getLexerFor(self, filePath):
        # set a lexer
        file_ext = os.path.splitext(str(filePath).lower())[-1]
        lexer = None
        parser = ConfigParser()
        config_file_path = pathlib.Path(__file__).parent / "config.ini"
        assert os.path.exists(
            config_file_path
        ), f"FATAL: Configuration file {config_file_path} does not exist!"
        parser.read(config_file_path)

        if file_ext in [".py"]:
            # using Visual Studio Code scheme
            lexer = QsciLexerPython()
            logger.info(f"Using QsciLexerPython for {filePath}")

            section = "PYTHON"
            assert parser.has_section(
                section
            ), f"FATAL: unable to find section for {section} in configuration file!"

            # lexer.setDefaultColor(QColor("#D4D4D4"))
            # lexer.setDefaultColor(QColor("#D4D4D4"))
            lexer.setDefaultColor(QColor(parser[section]["default"]))
            lexer.setDefaultFont(self._editorFont)

            lexer.setFont(self._editorFont, QsciLexerPython.Comment)
            # lexer.setColor(QColor("#6A8759"), QsciLexerPython.Comment)
            lexer.setColor(
                QColor(parser[section]["comment_line"]), QsciLexerPython.Comment
            )
            lexer.setFont(self._editorFont, QsciLexerPython.CommentBlock)
            # lexer.setColor(QColor("#6A8759"), QsciLexerPython.CommentBlock)
            lexer.setColor(
                QColor(parser[section]["comment_block"]), QsciLexerPython.CommentBlock
            )

            lexer.setFont(self._editorFont, QsciLexerPython.Keyword)
            # lexer.setColor(QColor("#569CD6"), QsciLexerPython.Keyword)
            lexer.setColor(QColor(parser[section]["keyword"]), QsciLexerPython.Keyword)

            lexer.setFont(self._editorFont, QsciLexerPython.ClassName)
            # lexer.setColor(QColor("#4EC9B0"), QsciLexerPython.ClassName)
            lexer.setColor(
                QColor(parser[section]["classname"]), QsciLexerPython.ClassName
            )
            lexer.setFont(self._editorFont, QsciLexerPython.FunctionMethodName)
            # lexer.setColor(QColor("#C586C0"), QsciLexerPython.FunctionMethodName)
            lexer.setColor(
                QColor(parser[section]["function"]), QsciLexerPython.FunctionMethodName
            )
            lexer.setFont(self._editorFont, QsciLexerPython.Number)
            # lexer.setColor(QColor("#B5CEA8"), QsciLexerPython.Number)
            lexer.setColor(QColor(parser[section]["number"]), QsciLexerPython.Number)

            lexer.setFont(self._editorFont, QsciLexerPython.SingleQuotedString)
            # lexer.setColor(QColor("#CE9178"), QsciLexerPython.SingleQuotedString)
            lexer.setColor(
                QColor(parser[section]["single_quoted_string"]),
                QsciLexerPython.SingleQuotedString,
            )
            lexer.setFont(self._editorFont, QsciLexerPython.DoubleQuotedString)
            # lexer.setColor(QColor("#CE9178"), QsciLexerPython.DoubleQuotedString)
            lexer.setColor(
                QColor(parser[section]["double_quoted_string"]),
                QsciLexerPython.DoubleQuotedString,
            )

            lexer.setFont(self._editorFont, QsciLexerPython.TripleSingleQuotedString)
            # lexer.setColor(QColor("#CE9178"), QsciLexerPython.TripleSingleQuotedString)
            lexer.setColor(
                QColor(parser[section]["triple_quoted_string"]),
                QsciLexerPython.TripleSingleQuotedString,
            )
            lexer.setFont(self._editorFont, QsciLexerPython.TripleDoubleQuotedString)
            # lexer.setColor(QColor("#CE9178"), QsciLexerPython.TripleDoubleQuotedString)
            lexer.setColor(
                QColor(parser[section]["triple_quoted_string"]),
                QsciLexerPython.TripleDoubleQuotedString,
            )

            lexer.setFont(self._editorFont, QsciLexerPython.SingleQuotedFString)
            # lexer.setColor(QColor("#CE9178"), QsciLexerPython.SingleQuotedFString)
            lexer.setColor(
                QColor(parser[section]["single_quoted_string"]),
                QsciLexerPython.SingleQuotedFString,
            )
            lexer.setFont(self._editorFont, QsciLexerPython.DoubleQuotedFString)
            lexer.setColor(QColor("#CE9178"), QsciLexerPython.DoubleQuotedFString)

            lexer.setFont(self._editorFont, QsciLexerPython.TripleSingleQuotedFString)
            lexer.setColor(QColor("#CE9178"), QsciLexerPython.TripleSingleQuotedFString)
            lexer.setFont(self._editorFont, QsciLexerPython.TripleDoubleQuotedFString)
            lexer.setColor(QColor("#CE9178"), QsciLexerPython.TripleDoubleQuotedFString)

        elif file_ext in [".h", ".hpp", ".hxx", ".c", ".cc", ".cpp"]:
            lexer = QsciLexerCPP()
            logger.info(f"Using QsciLexerCPP for {filePath}")
            lexer.setFont(self._editorFontItalic, QsciLexerCPP.Comment)
            lexer.setColor(QColor("#57A64A"), QsciLexerCPP.Comment)
            lexer.setFont(self._editorFontItalic, QsciLexerCPP.CommentLine)
            lexer.setColor(QColor("#57A64A"), QsciLexerCPP.CommentLine)
            lexer.setFont(self._editorFontItalic, QsciLexerCPP.PreProcessorComment)
            lexer.setColor(QColor("#57A64A"), QsciLexerCPP.PreProcessorComment)
            lexer.setFont(self._editorFontItalic, QsciLexerCPP.CommentDoc)
            lexer.setColor(QColor("#57A64A"), QsciLexerCPP.CommentDoc)

            lexer.setFont(self._editorFont, QsciLexerCPP.Keyword)
            lexer.setColor(QColor("#C586C0"), QsciLexerCPP.Keyword)
            lexer.setFont(self._editorFont, QsciLexerCPP.KeywordSet2)
            lexer.setColor(QColor("#C586C0"), QsciLexerCPP.KeywordSet2)
            lexer.setFont(self._editorFont, QsciLexerCPP.GlobalClass)
            lexer.setColor(QColor("#C586C0"), QsciLexerCPP.GlobalClass)

            lexer.setFont(self._editorFont, QsciLexerCPP.PreProcessor)
            lexer.setColor(QColor("#569CD6"), QsciLexerCPP.PreProcessor)

            lexer.setFont(self._editorFont, QsciLexerCPP.Identifier)
            lexer.setColor(QColor("#ffffff"), QsciLexerCPP.Identifier)
            lexer.setFont(self._editorFont, QsciLexerCPP.Number)
            lexer.setColor(QColor("#4EC9B0"), QsciLexerCPP.Number)

            lexer.setFont(self._editorFont, QsciLexerCPP.SingleQuotedString)
            lexer.setColor(QColor("#D69D85"), QsciLexerCPP.SingleQuotedString)
            lexer.setFont(self._editorFont, QsciLexerCPP.DoubleQuotedString)
            lexer.setColor(QColor("#D69D85"), QsciLexerCPP.DoubleQuotedString)

            lexer.setFont(self._editorFont, QsciLexerCPP.RawString)
            lexer.setColor(QColor("#D69D85"), QsciLexerCPP.RawString)
            lexer.setFont(self._editorFont, QsciLexerCPP.VerbatimString)
            lexer.setColor(QColor("#D69D85"), QsciLexerCPP.VerbatimString)

            lexer.setFont(self._editorFont, QsciLexerCPP.Default)
            lexer.setColor(QColor("#ffffff"), QsciLexerCPP.Default)
            lexer.setFont(self._editorFont, QsciLexerCPP.Operator)
            lexer.setColor(QColor("#ffffff"), QsciLexerCPP.Operator)

        elif file_ext in [".java"]:
            lexer = QsciLexerJava()
        # TODO: add others
        lexer.setDefaultFont(self._editorFont)
        return lexer

    def open(self):
        file_filters = (
            "Python Files (*.py);; C/C++ Files (*.h *.hxx *.c *.C *.cc *.CC *.cpp);;"
            "Java Files (*.java);; Text Files (*.txt)"
        )
        default_filter = "Python Files (*.py)"
        startupDir = os.path.dirname(__file__)
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a file to load",
            directory=startupDir,
            filter=file_filters,
            initialFilter=default_filter,
        )
        if response[0] != "":
            self.loadTextFile(response[0])

    def loadTextFile(self, filePath):
        if os.path.exists(filePath):
            with open(filePath, "r") as f:
                txt = f.read()
                self._editor.setText(txt)
                self.setWindowTitle(
                    f"PyQt {PYQT_VERSION_STR} Text Editor: {os.path.basename(filePath)}"
                )
                del self._lexer
                self._lexer = self.getLexerFor(filePath)
                self._editor.setLexer(self._lexer)
                print(f"Loaded file: {filePath}")


def main():
    ap = ArgumentParser()
    ap.add_argument(
        "-f", "--file", required=False, help="Full path of text file to edit"
    )
    args = vars(ap.parse_args())

    chocolaf.enable_hi_dpi()
    app = chocolaf.ChocolafApp(sys.argv)
    app.setStyle("WindowsDark")
    # app = QApplication(sys.argv)
    # app.setStyle("Fusion")

    w = TextEditorWindow()
    w.setWindowTitle(f"PyQt {PYQT_VERSION_STR} Text Editor")
    # w.loadTextFile(os.path.join(os.path.dirname(__file__), "TextEditor.py"))

    if args["file"] is not None:
        # check if image path provided
        if os.path.exists(args["file"]):
            print(f"Will open {args['file']} for editing")
            w.loadTextFile(args["file"])
        else:
            print(f"WARNING: {args['file']} - path does not exist!")
    # else:
    #     #w._editor.setText("Hello World! Welcome to QScintilla based text editing!\n\tThis illustrates\n\tindentation")
    #     w.loadTextFile(os.path.join(os.path.dirname(__file__), "TextEditor.py"))
    w.loadTextFile(
        r"C:\Dev\Code\git-projects\ChocolafStyle\examples\Python\MyProjects\Database\createDatabase.py"
    )
    w.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
