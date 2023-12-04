"""
queryPad: a PostgreSQL query application with a very basic SQL syntax editor.

@author: Manish Bhobe
This code is released for research purposed only. Please use at your own risk!
"""

import sys
import pathlib
from configparser import ConfigParser
import datetime
import logging

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *

import chocolaf

from syntaxeditor import TextEditor, SqlSyntaxHighlighter


logger = logging.getLogger(__name__)


class ActionBtn(QPushButton):
    def __init__(self, action: QAction, parent: QWidget = None):
        super().__init__(parent)
        self.setIcon(action.icon())
        self.setText(action.text())
        self.clicked.connect(action.trigger)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.db_conn = None

        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR} SQL Query Viewer")
        self.resize(800, 600)
        icon_path = pathlib.Path(__file__).parent / "database.png"
        self.setWindowIcon(QIcon(str(icon_path)))

        run_icon_path = pathlib.Path(__file__).parent / "play.png"
        self.runAction = QAction(QIcon(str(run_icon_path)), "&Run Query", self)
        self.runAction.setShortcut("Ctrl+R")
        self.runAction.setStatusTip("Run Query")
        self.runAction.triggered.connect(self.run_query)

        self.query_edit = TextEditor()

        self.highlighter = SqlSyntaxHighlighter(self.query_edit.document())
        self.query_edit.setPlaceholderText(
            "Enter your SQL query here and press Ctrl+R to run..."
        )
        self.query_edit.textChanged.connect(self.queryTextChanged)

        self.run_query_button = ActionBtn(self.runAction)  # QPushButton("Run Query")
        self.run_query_button.setEnabled(False)

        # setup a shortcut
        self.execQuery = QShortcut("Ctrl+R", self)
        self.execQuery.setEnabled(False)
        self.execQuery.activated.connect(self.run_query)

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

        self.setLayout(self.layout)

    def connect(self) -> QSqlDatabase:
        config_path = pathlib.Path(__file__).parent / "connect.ini"
        if config_path.exists():
            parser = ConfigParser()
            parser.read(str(config_path))
            # read connection params from config file
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

    def queryTextChanged(self):
        query_text = self.query_edit.toPlainText()
        has_text: bool = len(query_text) > 0
        self.run_query_button.setEnabled(has_text)
        self.runAction.setEnabled(has_text)
        self.execQuery.setEnabled(has_text)

    def show_fatal_message(self, message):
        """Shows a fatal message using QMessageBox.

        Args:
            message: The message to display.
        """
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Icon.Critical)
        msgBox.setText(message)
        msgBox.setWindowTitle("SQL Execution Error")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        return msgBox.exec()

    def run_query(self):
        """
        run query entered in the text box - if there is a selection,
        execute the selection else run entire content
        """

        # if text is selected, execure selected text,
        # else execute all the text in query_text widget
        if self.query_edit.textCursor().hasSelection():
            query_text = self.query_edit.textCursor().selection().toPlainText().strip()
            # query_text = query_text.toPlainText().strip()
        else:
            query_text = self.query_edit.toPlainText().strip()
        logger.info(f"Executing: {query_text}")

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
            return self.show_fatal_message(query.lastError().text())

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
    chocolaf.enable_hi_dpi()
    app = chocolaf.ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")
    app.setStyle("WindowsDark")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
