"""
queryPad: a PostgreSQL query application with a SQL syntax editor (very basic)
@author: Manish Bhobe
This code is released for research purposed only. Please use at your own risk!
"""

import sys
import pathlib
from configparser import ConfigParser
import datetime

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *

from syntaxeditor import TextEditor, SqlSyntaxHighlighter


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.db_conn = None

        self.setWindowTitle("PyQt6 SQL Query Viewer")
        self.resize(800, 600)

        # self.query_edit = QTextEdit()  # QLineEdit()
        # editor_font = QFont("Monospace", 10)
        # editor_font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        # self.query_edit.setFont(editor_font)
        # # set tabstops to 4 spaces
        # font = self.query_edit.font()
        # fontMetrics = QFontMetrics(font)
        # spaceWidth = fontMetrics.averageCharWidth()
        # self.query_edit.setTabStopDistance(spaceWidth * 4)
        # # set linespacing to 1.5 times
        # self.query_edit.setStyleSheet("line-height: 200%;")
        self.query_edit = TextEditor()

        self.highlighter = SqlSyntaxHighlighter(self.query_edit.document())
        # self.highlighter.set_parent(self.query_edit)
        self.query_edit.setPlaceholderText("Enter a SQL query...")

        self.run_query_button = QPushButton("Run Query")
        self.run_query_button.clicked.connect(self.run_query)

        self.topWidget = QWidget()
        topLayout = QVBoxLayout()
        l2 = QHBoxLayout()
        l2.addStretch()
        l2.addWidget(self.run_query_button)
        topLayout.addWidget(self.query_edit)
        topLayout.addLayout(l2)
        self.topWidget.setLayout(topLayout)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(0)
        self.results_table.setHorizontalHeaderLabels([])
        self.results_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.topWidget)
        self.splitter.addWidget(self.results_table)
        self.splitter.setSizes((20, 80))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.splitter)
        # self.addWidget(self.splitter)

        # self.layout = QGridLayout()
        # self.layout.addWidget(self.query_edit, 0, 0, 1, 2)
        # self.layout.addWidget(self.run_query_button, 1, 0)
        # self.layout.addWidget(self.results_table, 2, 0, 1, 2)

        self.setLayout(self.layout)

    def connect(self) -> QSqlDatabase:
        config_path = pathlib.Path(__file__).parent / "connect.ini"
        if config_path.exists():
            parser = ConfigParser()
            parser.read(str(config_path))
            # connection_params = {}
            section_name = "postgres_dvdrental"
            if parser.has_section(section_name):
                conn = QSqlDatabase.addDatabase("QPSQL", "postgres_dvdrental")
                conn.setHostName(parser.get(section_name, "host"))
                conn.setDatabaseName(parser.get(section_name, "database"))
                conn.setUserName(parser.get(section_name, "user_name"))
                conn.setPassword(parser.get(section_name, "password"))
                # connect
                conn.open()
                return conn
            else:
                raise IOError(
                    f"Found {str(config_path)}! But it does not have a 'postgres_dvdrental' entry!"
                )
        else:
            raise IOError(
                f"Unable to locate {str(config_path)} to read db connection params!"
            )

    def show_fatal_message(self, message):
        """Shows a fatal message using QMessageBox.

        Args:
            message: The message to display.
        """
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Critical)
        msgBox.setText(message)
        msgBox.setWindowTitle("Database Error")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def run_query(self):
        # query_text = self.query_edit.text().strip()
        query_text = self.query_edit.toPlainText().strip()

        # Connect to the database
        if self.db_conn is None:
            self.db_conn = self.connect()
            if not self.db_conn.isOpen():
                self.show_fatal_message(self.db_conn.lastError().text())
                sys.exit("Could not open database")

        # Prepare the query
        query = QSqlQuery(self.db_conn)

        # Execute the query
        if not query.exec(query_text):
            # self.show_fatal_message(
            #     f"Could not execute query: {}"
            # )
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.setText(query.lastError().text())
            msgBox.setWindowTitle("SQL Execution Error")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
            return msgBox.exec()

        # Get the column names
        column_names = [
            query.record().fieldName(i) for i in range(query.record().count())
        ]

        # Set the column headers
        self.results_table.setColumnCount(len(column_names))
        self.results_table.setHorizontalHeaderLabels(column_names)

        # Clear the table
        self.results_table.setRowCount(0)

        # Iterate over the results
        while query.next():
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)

            # Get the values of the current row
            values = [query.value(i) for i in range(query.record().count())]

            # Format the values per the locale used
            locale = QLocale()
            for i in range(len(values)):
                value = values[i]
                if isinstance(value, datetime.datetime):
                    value = value.toDateTime()
                    value = locale.toString(value, Qt.DateFormat.ShortFormat)
                elif isinstance(value, QDate):
                    # value = value.toDataTime()
                    value = locale.toString(value, QLocale.FormatType.ShortFormat)
                elif isinstance(value, QDateTime):
                    # value = value.toDataTime()
                    value = locale.toString(value, QLocale.FormatType.ShortFormat)
                elif isinstance(value, datetime.date):
                    value = value.toDate()
                    value = locale.toString(value, Qt.DateFormat.ShortFormat)
                elif isinstance(value, float):
                    value = value.toFloat()
                    value = locale.toString(value, Qt.FormatStyle.DecimalFormat)

                # Set the item in the table
                item = QTableWidgetItem(str(value))
                self.results_table.setItem(row, i, item)
        del query


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
