import sys
import os
import pathlib
from configparser import ConfigParser

from PyQt6.QtCore import Qt, QLocale, QRegularExpression
from PyQt6.QtGui import *

from .sectionParser import parseSection


class SqlSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, doc: QTextDocument):
        super(QSyntaxHighlighter, self).__init__(doc)

        self.keywords_pat, self.keyword_format = parseSection(
            "SQL",
            "sql_keywords",
        )
        self.data_types_pat, self.data_types_format = parseSection(
            "SQL",
            "sql_data_types",
        )
        self.sql_functions_pat, self.sql_functions_format = parseSection(
            "SQL",
            "sql_functions",
        )
        _, self.sql_strings_format = parseSection(
            "SQL",
            "sql_string",
        )
        _, self.sql_number_format = parseSection(
            "SQL",
            "sql_number",
        )
        _, self.sql_comment_format = parseSection(
            "SQL",
            "sql_comment",
        )

        # self.config_file_path = pathlib.Path(__file__).parent / "syntax.ini"
        # self.section = "SQL"

        # # read keywords etc. from syntax.ini/SQL section
        # assert os.path.exists(
        #     str(self.config_file_path)
        # ), f"FATAL ERROR: unable to locate syntax configuration file (syntax.ini)"
        # parser = ConfigParser()
        # parser.read(str(self.config_file_path))
        # assert parser.has_section(
        #     self.section
        # ), f"FATAL ERROR: expecting section [SQL] in syntax config file (syntax.ini)"

        # # keywords settings
        # self.sep_pat = r"\b"
        # keywords_str = parser.get(self.section, "sql_keywords")
        # keywords = keywords_str.split(",")
        # self.keywords_pat = ""
        # for kw in keywords:
        #     kw = f"{self.sep_pat}{kw.strip()}{self.sep_pat}|"
        #     self.keywords_pat += kw
        # if self.keywords_pat.endswith("|"):
        #     self.keywords_pat = self.keywords_pat[: len(self.keywords_pat) - 1]
        # keywords_color_style = parser.get(self.section, "sql_keywords_color_style")
        # keywords_color, keywords_bold, keywords_italic = keywords_color_style.split(",")
        # keywords_font_bold = True if keywords_bold.strip() == "1" else False
        # keywords_font_italic = True if keywords_italic.strip() == "1" else False
        # # define formatter for keywords
        # self.keyword_format = QTextCharFormat()
        # self.keyword_format.setForeground(QBrush(QColor(keywords_color)))
        # if keywords_font_bold:
        #     self.keyword_format.setFontWeight(QFont.Weight.Bold)
        # if keywords_font_italic:
        #     self.keyword_format.setFontItalic(True)

        # # data type settings
        # data_types_str = parser.get(self.section, "sql_data_types")
        # data_types = data_types_str.split(",")
        # self.data_types_pat = ""
        # for dt in data_types:
        #     dt = f"{self.sep_pat}{dt.strip()}{self.sep_pat}|"
        #     self.data_types_pat += dt
        # if self.data_types_pat.endswith("|"):
        #     self.data_types_pat = self.data_types_pat[: len(self.data_types_pat) - 1]
        # data_types_color_style = parser.get(self.section, "sql_data_types_color_style")
        # dt_color, dt_bold, dt_italic = data_types_color_style.split(",")
        # dt_font_bold = True if dt_bold.strip() == "1" else False
        # dt_font_italic = True if dt_italic.strip() == "1" else False
        # # data types formatter
        # self.data_types_format = QTextCharFormat()
        # self.data_types_format.setForeground(QBrush(QColor(dt_color)))
        # if dt_font_bold:
        #     self.data_types_format.setFontWeight(QFont.Weight.Bold)
        # if dt_font_italic:
        #     self.data_types_format.setFontItalic(True)

        # # sql functions
        # sql_functions_str = parser.get(self.section, "sql_functions")
        # sql_functions = sql_functions_str.split(",")
        # self.sql_functions_pat = ""
        # for fxn in sql_functions:
        #     fxn = f"{self.sep_pat}{fxn.strip()}{self.sep_pat}|"
        #     self.sql_functions_pat += fxn
        # if self.sql_functions_pat.endswith("|"):
        #     self.sql_functions_pat = self.sql_functions_pat[
        #         : len(self.sql_functions_pat) - 1
        #     ]
        # sql_functions_color_style = parser.get(
        #     self.section, "sql_functions_color_style"
        # )
        # fxn_color, fxn_bold, fxn_italic = sql_functions_color_style.split(",")
        # fxn_font_bold = True if fxn_bold.strip() == "1" else False
        # fxn_font_italic = True if fxn_italic.strip() == "1" else False
        # # sql functions formatter
        # self.sql_functions_format = QTextCharFormat()
        # self.sql_functions_format.setForeground(QBrush(QColor(fxn_color)))
        # if fxn_font_bold:
        #     self.sql_functions_format.setFontWeight(QFont.Bold)
        # if fxn_font_italic:
        #     self.sql_functions_format.setFontItalic(True)

        # # string style
        # sql_strings_color_style = parser.get(self.section, "sql_string_color_style")
        # str_color, str_bold, str_italic = sql_strings_color_style.split(",")
        # str_font_bold = True if str_bold.strip() == "1" else False
        # str_font_italic = True if str_italic.strip() == "1" else False
        # # sql strings formatter
        # self.sql_strings_format = QTextCharFormat()
        # self.sql_strings_format.setForeground(QBrush(QColor(str_color)))
        # if str_font_bold:
        #     self.sql_strings_format.setFontWeight(QFont.Bold)
        # if str_font_italic:
        #     self.sql_strings_format.setFontItalic(True)

        # # numbers style
        # sql_number_color_style = parser.get(self.section, "sql_number_color_style")
        # number_color, number_bold, number_italic = sql_number_color_style.split(",")
        # number_font_bold = True if number_bold.strip() == "1" else False
        # number_font_italic = True if number_italic.strip() == "1" else False
        # # sql number formatter
        # self.sql_number_format = QTextCharFormat()
        # self.sql_number_format.setForeground(QBrush(QColor(number_color)))
        # if number_font_bold:
        #     self.sql_number_format.setFontWeight(QFont.Bold)
        # if number_font_italic:
        #     self.sql_number_format.setFontItalic(True)

        # # comments style
        # sql_comment_color_style = parser.get(self.section, "sql_comment_color_style")
        # comment_color, comment_bold, comment_italic = sql_comment_color_style.split(",")
        # comment_font_bold = True if comment_bold.strip() == "1" else False
        # comment_font_italic = True if comment_italic.strip() == "1" else False
        # # sql comment formatter
        # self.sql_comment_format = QTextCharFormat()
        # self.sql_comment_format.setForeground(QBrush(QColor(comment_color)))
        # if comment_font_bold:
        #     self.sql_comment_format.setFontWeight(QFont.Bold)
        # if comment_font_italic:
        #     self.sql_comment_format.setFontItalic(True)

    def highlightBlock(self, text):
        # formatters
        # Define the rules for highlighting SQL and Python code
        rules = [
            (
                # SQL keywords
                QRegularExpression(
                    self.keywords_pat,
                    QRegularExpression.PatternOption.CaseInsensitiveOption,
                ),
                self.keyword_format,
            ),
            (
                # SQL datatypes
                QRegularExpression(
                    self.data_types_pat,
                    QRegularExpression.PatternOption.CaseInsensitiveOption,
                ),
                self.data_types_format,
            ),
            (
                # SQL functions
                QRegularExpression(
                    self.sql_functions_pat,
                    QRegularExpression.PatternOption.CaseInsensitiveOption,
                ),
                self.sql_functions_format,
            ),
            (
                # strings
                QRegularExpression(r"'[^']*'"),
                self.sql_strings_format,
            ),
            (
                # numbers
                QRegularExpression(r"\d+"),
                self.sql_number_format,
            ),
            (
                # single line comments
                QRegularExpression(r"-{2,}\s+.+"),
                self.sql_comment_format,
            ),
            (
                # multi line comments
                QRegularExpression(r"/\*.*\*/"),
                self.sql_comment_format,
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
