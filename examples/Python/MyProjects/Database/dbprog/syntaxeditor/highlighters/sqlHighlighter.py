from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QTextDocument, QSyntaxHighlighter

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

        # Define the rules for highlighting SQL code
        self.rules = [
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

    def highlightBlock(self, text):
        # formatters
        for rule in self.rules:
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
