import sys
import os
import pathlib
from configparser import ConfigParser

from PyQt6.QtCore import Qt, QLocale, QRegularExpression
from PyQt6.QtGui import *

from .sectionParser import parseSection


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, doc: QTextDocument):
        super(QSyntaxHighlighter, self).__init__(doc)

        self.keywords_pat, self.keywords_format = parseSection(
            "Python",
            "python_keywords",
        )
        self.dunder_pat, self.dunder_format = parseSection(
            "Python", "python_dunder_fxns"
        )
        self.built_in_pat, self.built_in_format = parseSection(
            "Python", "python_built_in_fxns"
        )
        self.special_pat, self.special_format = parseSection(
            "Python",
            "python_special_fxns",
        )
        _, self.number_format = parseSection(
            "Python",
            "python_number",
        )
        _, self.string_format = parseSection(
            "Python",
            "python_string",
        )
        _, self.comment_format = parseSection(
            "Python",
            "python_comment",
        )

    def highlightBlock(self, text):
        # formatters
        # Define the rules for highlighting SQL and Python code
        rules = [
            (
                # Python keywords
                QRegularExpression(self.keywords_pat),
                self.keywords_format,
            ),
            (
                # Python dunder functions
                # such as __init__, __gt__, __getitem__ etc.
                QRegularExpression(self.dunder_pat),
                self.dunder_format,
            ),
            (
                # Python built-in functions
                # such as print,ord,round etc.
                QRegularExpression(self.built_in_pat),
                self.built_in_format,
            ),
            (
                # Python special functions
                # such as self, None, True, False
                QRegularExpression(self.special_pat),
                self.special_format,
            ),
            (
                # single quoted strings
                QRegularExpression(r"'[^']*'"),
                self.string_format,
            ),
            (
                # double quoted strings
                QRegularExpression(r"\"[^\"]*\""),
                self.string_format,
            ),
            (
                # triple quoted strings
                # NOTE: these can span multiple lines
                QRegularExpression(
                    r'\'\'\'(.*?)\'\'\'|"""(.*?)"""',
                    QRegularExpression.PatternOption.DotMatchesEverythingOption,
                ),
                self.string_format,
            ),
            (
                # numbers (numbers delimited by at least 1 whitespace)
                QRegularExpression(r"\s+\d+\s+"),
                self.number_format,
            ),
            (
                # comments
                QRegularExpression(r"#\s*.+"),
                self.comment_format,
            ),
        ]

        # Highlight the text in the document
        for rule in rules:
            matches = rule[0].globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule[1])
                # print(
                #     f"start: {match.capturedStart()} - len: {match.capturedLength()} - content: {match.captured()}"
                # )


if __name__ == "__main__":
    txt = """
select c.first_name, c.last_name, c.email,
    a.address, a.district, ci.city, ct.country, a.postal_code, a.phone
from customer as c
join address as a on c.address_id = a.address_id
join city as ci on a.city_id = ci.city_id
join country as ct on ci.country_id = ct.country_id
where c.first_name like 'J%' and c.last_name like 'W%'
"""
    from PyQt6.QtWidgets import QTextEdit, QApplication

    app = QApplication([])
    editor = QTextEdit()
    hl = SqlSyntaxHighlighter(editor.document())
    hl.highlightBlock(txt)
