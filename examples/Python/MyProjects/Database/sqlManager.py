#!/usr/bin/env python
"""
* sqlManager.sql - interface for SQL queries
* @author (Chocolaf): Manish Bhobe
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys
import os
import argparse

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

from chocolaf.utils.chocolafapp import ChocolafApp
import toolbarIcons_rc


# print(f"os.environ['QT_DEBUG_PLUGINS'] = {os.environ['QT_DEBUG_PLUGINS']}")
THIS_DIR = os.path.dirname(__file__)
DB_VENDOR = "QSQLITE"
DB_NAME = os.path.join(THIS_DIR, "databases", "FishingStores.sqlite")


def connectToDatabase() -> QSqlDatabase:
    conn = QSqlDatabase.addDatabase(DB_VENDOR, "con1")
    conn.setDatabaseName(DB_NAME)
    if not conn.open():
        errMsg = f"FATAL: unable to connect to database {DB_NAME}."
        errMsg += f"\nConnection Error: {conn.lastError().databaseText()}"
        QMessageBox.critical(None, "FATAL ERROR", errMsg)
        return None
    return conn


class SQLManager(QMainWindow):
    def __init__(self, dbConn: QSqlDatabase, parent: QWidget = None):
        super(SQLManager, self).__init__(parent)
        self.conn = dbConn
        self.initializeUi()

    def initializeUi(self):
        """ initialize the Ui """
        self.setMinimumSize(800, 550)
        # center on screen
        self.move(QApplication.desktop().screen().rect().center() -
                  self.rect().center())
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR}: SQLManager")
        self.model = QSqlQueryModel()
        self.setupWindow()
        self.setupToolbar()
        self.setWindowIcon(QIcon(":/sql_manager.png"))

    def setupWindow(self):
        self.queryField = QTextEdit()
        self.queryField.setFont(QFont("Consolas, SF Mono, Monospace", 10))
        self.queryField.setPlaceholderText("Enter your SQL query here and press Ctrl+R to run...")

        self.results = QTableView()
        self.results.setAlternatingRowColors(True)
        self.results.setModel(self.model)
        self.results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results.hideColumn(0)

        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.queryField)
        self.splitter.addWidget(self.results)
        # divide 30:70 ratios
        self.splitter.setSizes((20, 80))

        # setup a shortcut
        self.execQuery = QShortcut("Ctrl+R", self)
        self.execQuery.activated.connect(self.executeQueries)

        layout = QVBoxLayout()
        layout.addWidget(self.splitter)

        mainContainer = QWidget()
        # mainContainer.setObjectName("mainContainer")
        # mainContainer.setStyleSheet("QWidget#mainContainer {border:None;}")
        mainContainer.setLayout(layout)
        self.setCentralWidget(mainContainer)

    def setupToolbar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.RightToolBarArea, toolbar)

        clearTextAction = QAction(QIcon(":/edit_delete.png"), "Clear Queries",
                                  toolbar)
        clearTextAction.setToolTip("Clear all queries in text field")
        clearTextAction.triggered.connect(self.clearText)

        runQueryAction = QAction(QIcon(":/playback_play.png"), "Run Queries",
                                 toolbar)
        runQueryAction.setToolTip("Run all queries entered")
        runQueryAction.triggered.connect(self.executeQueries)

        quitAction = QAction(QIcon(":/on-off.png"), "Quit Application", toolbar)
        quitAction.setToolTip("Quit the application")
        quitAction.triggered.connect(qApp.exit)

        toolbar.addAction(runQueryAction)
        toolbar.addAction(clearTextAction)
        toolbar.addSeparator()
        toolbar.addAction(quitAction)

    def executeQueries(self):
        sqlQueryTexts = self.queryField.toPlainText().strip()  # str(self.queryField.textCursor().selectedText())
        sqlQueryTexts = sqlQueryTexts.split("\n")

        if sqlQueryTexts != "":
            # queries cannot have \n characters in them (strange!)
            for sqlQueryText in sqlQueryTexts:
                if sqlQueryText == "":
                    pass
                else:
                    #sqlQueryText = " ".join(sqlQueryText.split("\n"))
                    print(f"Exec: {sqlQueryText}")
                    query = QSqlQuery(sqlQueryText, self.conn)
                    self.model.setQuery(query)
                    # self.results.setModel(self.model)
                    # self.results.hideColumn(0)

    def clearText(self):
        self.queryField.clear()


if __name__ == "__main__":
    app = ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")
    #app = QApplication(sys.argv)

    try:
        conn = connectToDatabase()
        if (conn and conn.isOpen()):
            window = SQLManager(conn)
            window.show()
            app.exec()
        else:
            app.quit()
    finally:
        if conn:
            conn.close()
