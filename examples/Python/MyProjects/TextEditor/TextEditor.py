#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
* TextEditor.py - code editor using QScintilla
* @author (Chocolaf): Manish Bhobe
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import os
import sys
from argparse import ArgumentParser

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *

from chocolaf.utils.chocolafapp import ChocolafApp
from chocolaf.palettes import ChocolafPalette


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
        self.resize(QGuiApplication.primaryScreen().availableSize() * (4 / 5))
        self.setupEditor()
        self.setupActions()
        self.setupMenu()
        self.setCentralWidget(self._editor)

    def setupActions(self):
        # open image
        self.openAction = QAction("&Open...", self)
        self.openAction.setShortcut(QKeySequence.New)
        # self.openAction.setIcon(QIcon(":/open.png"))
        self.openAction.setStatusTip("Open a file")
        self.openAction.triggered.connect(self.open)

        # exit
        self.exitAction = QAction("E&xit", self)
        self.exitAction.setShortcut(QKeySequence("Ctrl+Q"))
        self.exitAction.setStatusTip("Exit the application")
        self.exitAction.triggered.connect(QApplication.instance().quit)

    def setupMenu(self):
        # file menu
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

    def setupEditor(self):
        self._editorFont = QFont("Noto Mono, Consolas, SF Mono, Menlo, Monaco, DejaVu Sans Mono, Monospace")
        self._editorFont.setPointSize(10)
        self._editorFontBold = QFont("Noto Mono, Consolas, SF Mono, Menlo, Monaco, DejaVu Sans Mono, Monospace")
        self._editorFontBold.setPointSize(10)
        self._editorFontBold.setBold(True)
        self._editorFontItalic = QFont("Noto Mono, Consolas, SF Mono, Menlo, Monaco, DejaVu Sans Mono, Monospace")
        self._editorFontItalic.setPointSize(10)
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
        self._editor.setCaretLineBackgroundColor(QColor("#1fff0000"))
        # setup margins
        self._editor.setMarginType(0, QsciScintilla.NumberMargin)
        self._editor.setMarginType(1, QsciScintilla.TextMargin)
        self._editor.setMarginWidth(0, "99999")
        self._editor.setMarginWidth(1, "99")
        self._editor.setMarginsBackgroundColor(ChocolafPalette.Button_Color)
        self._editor.setMarginsForegroundColor(ChocolafPalette.Disabled_Text_Color)

    def getLexerFor(self, filePath):
        # set a lexer
        file_ext = os.path.splitext(str(filePath).lower())[-1]
        lexer = None
        if file_ext in [".py"]:
            lexer = QsciLexerPython()
            lexer.setFont(self._editorFontItalic, QsciLexerPython.Comment)
            lexer.setColor(QColor('#57A64A'), QsciLexerPython.Comment)
            lexer.setFont(self._editorFontItalic, QsciLexerPython.CommentBlock)
            lexer.setColor(QColor('#57A64A'), QsciLexerPython.CommentBlock)

            lexer.setFont(self._editorFont, QsciLexerPython.Keyword)
            lexer.setColor(QColor('#C586C0'), QsciLexerPython.Keyword)

            lexer.setFont(self._editorFont, QsciLexerPython.ClassName)
            lexer.setColor(QColor('#569CD6'), QsciLexerPython.ClassName)
            lexer.setFont(self._editorFont, QsciLexerPython.FunctionMethodName)
            lexer.setColor(QColor('#4EC9B0'), QsciLexerPython.FunctionMethodName)
            lexer.setFont(self._editorFont, QsciLexerPython.Number)
            lexer.setColor(QColor('#4EC9B0'), QsciLexerPython.Number)

            lexer.setFont(self._editorFont, QsciLexerPython.SingleQuotedString)
            lexer.setColor(QColor('#D69D85'), QsciLexerPython.SingleQuotedString)
            lexer.setFont(self._editorFont, QsciLexerPython.DoubleQuotedString)
            lexer.setColor(QColor('#D69D85'), QsciLexerPython.DoubleQuotedString)

            lexer.setFont(self._editorFont, QsciLexerPython.TripleSingleQuotedString)
            lexer.setColor(QColor('#D69D85'), QsciLexerPython.TripleSingleQuotedString)
            lexer.setFont(self._editorFont, QsciLexerPython.TripleDoubleQuotedString)
            lexer.setColor(QColor('#D69D85'), QsciLexerPython.TripleDoubleQuotedString)

            lexer.setFont(self._editorFont, QsciLexerPython.SingleQuotedFString)
            lexer.setColor(QColor('#D69D85'), QsciLexerPython.SingleQuotedFString)
            lexer.setFont(self._editorFont, QsciLexerPython.DoubleQuotedFString)
            lexer.setColor(QColor('#D69D85'), QsciLexerPython.DoubleQuotedFString)

            lexer.setFont(self._editorFont, QsciLexerPython.TripleSingleQuotedFString)
            lexer.setColor(QColor('#D69D85'), QsciLexerPython.TripleSingleQuotedFString)
            lexer.setFont(self._editorFont, QsciLexerPython.TripleDoubleQuotedFString)
            lexer.setColor(QColor('#D69D85'), QsciLexerPython.TripleDoubleQuotedFString)

        elif file_ext in [".h", ".hpp", ".hxx", ".c", ".cc", ".cpp"]:
            lexer = QsciLexerCPP()
            lexer.setFont(self._editorFontItalic, QsciLexerCPP.Comment)
            lexer.setColor(QColor('#57A64A'), QsciLexerCPP.Comment)
            lexer.setFont(self._editorFontItalic, QsciLexerCPP.CommentLine)
            lexer.setColor(QColor('#57A64A'), QsciLexerCPP.CommentLine)
            lexer.setFont(self._editorFontItalic, QsciLexerCPP.PreProcessorComment)
            lexer.setColor(QColor('#57A64A'), QsciLexerCPP.PreProcessorComment)
            lexer.setFont(self._editorFontItalic, QsciLexerCPP.CommentDoc)
            lexer.setColor(QColor('#57A64A'), QsciLexerCPP.CommentDoc)

            lexer.setFont(self._editorFont, QsciLexerCPP.Keyword)
            lexer.setColor(QColor('#C586C0'), QsciLexerCPP.Keyword)
            lexer.setFont(self._editorFont, QsciLexerCPP.KeywordSet2)
            lexer.setColor(QColor('#C586C0'), QsciLexerCPP.KeywordSet2)
            lexer.setFont(self._editorFont, QsciLexerCPP.GlobalClass)
            lexer.setColor(QColor('#C586C0'), QsciLexerCPP.GlobalClass)

            lexer.setFont(self._editorFont, QsciLexerCPP.PreProcessor)
            lexer.setColor(QColor('#569CD6'), QsciLexerCPP.PreProcessor)


            lexer.setFont(self._editorFont, QsciLexerCPP.Identifier)
            lexer.setColor(QColor('#ffffff'), QsciLexerCPP.Identifier)
            lexer.setFont(self._editorFont, QsciLexerCPP.Number)
            lexer.setColor(QColor('#4EC9B0'), QsciLexerCPP.Number)

            lexer.setFont(self._editorFont, QsciLexerCPP.SingleQuotedString)
            lexer.setColor(QColor('#D69D85'), QsciLexerCPP.SingleQuotedString)
            lexer.setFont(self._editorFont, QsciLexerCPP.DoubleQuotedString)
            lexer.setColor(QColor('#D69D85'), QsciLexerCPP.DoubleQuotedString)

            lexer.setFont(self._editorFont, QsciLexerCPP.RawString)
            lexer.setColor(QColor('#D69D85'), QsciLexerCPP.RawString)
            lexer.setFont(self._editorFont, QsciLexerCPP.VerbatimString)
            lexer.setColor(QColor('#D69D85'), QsciLexerCPP.VerbatimString)

            lexer.setFont(self._editorFont, QsciLexerCPP.Default)
            lexer.setColor(QColor('#ffffff'), QsciLexerCPP.Default)
            lexer.setFont(self._editorFont, QsciLexerCPP.Operator)
            lexer.setColor(QColor('#ffffff'), QsciLexerCPP.Operator)

        elif file_ext in [".java"]:
            lexer = QsciLexerJava()
        # TODO: add others
        lexer.setDefaultFont(self._editorFont)
        return lexer

    def open(self):
        file_filters = "Python Files (*.py);; C/C++ Files (*.h *.hxx *.c *.C *.cc *.CC *.cpp);;"\
            "Java Files (*.java);; Text Files (*.txt)"
        default_filter = "Python Files (*.py)";
        startupDir = os.path.dirname(__file__)
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a file to load",
            directory=startupDir,
            filter=file_filters,
            initialFilter=default_filter
        )
        if response[0] != "":
            self.loadTextFile(response[0])


    def loadTextFile(self, filePath):
        if os.path.exists(filePath):
            with open(filePath, "r") as f:
                txt = f.read()
                self._editor.setText(txt)
                self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} Text Editor: {os.path.basename(filePath)}")
                del self._lexer
                self._lexer = self.getLexerFor(filePath)
                self._editor.setLexer(self._lexer)
                print(f"Loaded file: {filePath}")


def main():
    ap = ArgumentParser()
    ap.add_argument("-f", "--file", required=False,
                    help="Full path of text file to edit")
    args = vars(ap.parse_args())

    app = ChocolafApp(sys.argv)
    app.setStyle("Chocolaf")

    w = TextEditorWindow()
    w.setWindowTitle(f"PyQt {PYQT_VERSION_STR} Text Editor")
    # w.loadTextFile(os.path.join(os.path.dirname(__file__), "TextEditor.py"))

    if args['file'] is not None:
        # check if image path provided
        if os.path.exists(args['file']):
            print(f"Will open {args['file']} for editing")
            w.loadTextFile(args['file'])
        else:
            print(f"WARNING: {args['file']} - path does not exist!")
    # else:
    #     #w._editor.setText("Hello World! Welcome to QScintilla based text editing!\n\tThis illustrates\n\tindentation")
    #     w.loadTextFile(os.path.join(os.path.dirname(__file__), "TextEditor.py"))
    w.loadTextFile('/home/mjbhobe/code/git-projects/learning_Qt/bogo2bogo/ChocolafStyle/examples/C++/MyProjects/summerfield/spreadsheet/mainwindow.cpp')
    w.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
