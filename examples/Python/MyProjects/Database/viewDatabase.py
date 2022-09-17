#!/usr/bin/env python
"""
* viewDatabase.py: display results of a table or query in a QTableView
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
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

from chocolaf.utils.chocolafapp import ChocolafApp

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


def parseCommandLine():
    """ use argparse to parse out options from command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-model", type=str,
                        choices=["read-only", "read-write"], default="read-only",
                        help="Select the type of data model to view SQL data: " +
                        "read-only = QSqlQueryModel; read-write = QSqlTableModel")
    parser.add_argument("-q", "--query", type=str, default=["SELECT * FROM products"],
                        nargs="*", help="Pass a SQL query on the command line")
    args = vars(parser.parse_args())
    return args


class DisplayDatabase(QMainWindow):
    def __init__(self, dbConn: QSqlDatabase, parent: QWidget = None):
        super(DisplayDatabase, self).__init__(parent)
        self.conn = dbConn
        tables_needed = {'customers', 'stores', 'products', 'orders', 'order_products'}
        # get intersection of sets - must find at least some of the tables
        tables_not_found = tables_needed - set(self.conn.tables())
        if tables_not_found:
            QMessageBox.critical(self, "FATAL ERROR",
                                 f"Following tables are missing from database {tables_not_found}")
            sys.exit(-1)
        self.initializeUi()

    def initializeUi(self):
        """ initialize the Ui """
        self.setMinimumSize(800, 500)
        self.setWindowTitle(f"PyQt {PYQT_VERSION_STR}: Displaying SQL Data in Tables")
        self.setupTable(args["data_model"], args["query"])

    def setupTable(self, data_model, query_cmdline):
        self.model = QSqlQueryModel() if data_model == "read-only" else QSqlTableModel()
        # populate the model with data from query_cmdline
        for qry in query_cmdline:
            query = QSqlQuery(qry, self.conn)
            self.model.setQuery(query)

        tableView = QTableView()
        tableView.setModel(self.model)
        # comment line below if you want to see row numbers in first col of QTableView
        # (most won't want to see this)
        # tableView.hideColumn(0)
        tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setCentralWidget(tableView)


if __name__ == "__main__":
    app = ChocolafApp(sys.argv)
    # app.setStyle("Chocolaf")

    args = parseCommandLine()
    try:
        conn = connectToDatabase()
        if (conn and conn.isOpen()):
            window = DisplayDatabase(conn)
            window.show()
            app.exec()
        else:
            app.quit()
    finally:
        if conn:
            conn.close()
