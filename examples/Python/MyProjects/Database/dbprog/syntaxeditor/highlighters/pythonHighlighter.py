from PyQt6.QtCore import Qt, QLocale, QRegularExpression
from PyQt6.QtGui import QTextDocument, QSyntaxHighlighter

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

        self.rules = [
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
                    r"(\'\'\'|\"\"\")[\s\S]*?\1",
                    QRegularExpression.PatternOption.DotMatchesEverythingOption
                    | QRegularExpression.PatternOption.MultilineOption,
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

    def highlightBlock(self, text):
        # formatters
        # Define the rules for highlighting SQL and Python code

        # Highlight the text in the document
        for rule in self.rules:
            matches = rule[0].globalMatch(text)
            while matches.hasNext():
                match = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule[1])
                # print(
                #     f"start: {match.capturedStart()} - len: {match.capturedLength()} - content: {match.captured()}"
                # )


if __name__ == "__main__":
    code = """
import sys
import pathlib

this_path = pathlib.Path(__file__).parent

@decorator(param=1)
def nested_func(y):
    print(y + 1)

s = ("Test", 2+3, {'a': 'b'}, f'{x!s:{"^10"}}')   # Comment
f(s[0].lower())
nested_func(42)

class Foo:
    tags: List[str]

    def __init__(self: Foo):
        byte_string: bytes = b'newline:\n also newline:\x0a'
        normal_string: str = "Hello World!"
        self.make_sense(whatever=1)
    
    def make_sense[T](self, whatever: T):
        self.sense = whatever

x = len('abc')
type my_int = int
print(f.__doc__)
    """

    from PyQt6.QtWidgets import QTextEdit, QApplication
    import sys

    app = QApplication([])
    editor = QTextEdit()
    hl = PythonSyntaxHighlighter(editor.document())
    hl.highlightBlock(code)
    editor.setText(code)
    editor.show()
    sys.exit(app.exec())
