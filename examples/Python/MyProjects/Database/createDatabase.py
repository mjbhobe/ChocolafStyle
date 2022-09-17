#!/usr/bin/env python
"""
* createDatabase.py - create database objects for SQL demo
* @author (Chocolaf): Manish Bhobe
*
* My experiments with Python, PyQt, Data Science & Deep Learning
* The code is made available for illustration purposes only.
* Use at your own risk!!
"""
import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtSql import *

# print(f"os.environ['QT_DEBUG_PLUGINS'] = {os.environ['QT_DEBUG_PLUGINS']}")
THIS_DIR = os.path.dirname(__file__)
DB_VENDOR = "QSQLITE"
DB_NAME = os.path.join(THIS_DIR, "databases", "FishingStores.sqlite")


def connectToDatabase() -> QSqlDatabase:
    conn = QSqlDatabase.addDatabase(DB_VENDOR, "con1")
    conn.setDatabaseName(DB_NAME)
    if not conn.open():
        print(f"FATAL: unable to connect to database {DB_NAME}.")
        print(f"Connection Error: {conn.lastError().databaseText()}")
        return None
    else:
        print(f"SUCCESS! Connected to database {conn.databaseName()}")
        return conn


class CreateDatabaseObjects(QObject):
    def __init__(self, dbConn: QSqlDatabase, parent: QObject = None):
        super(CreateDatabaseObjects, self).__init__(parent)
        self.conn = dbConn
        self.createDbObjects()

    def createDbObjects(self):
        """ drop all db objects & create afresh """
        query = QSqlQuery(self.conn)

        # drop existing database objects
        print("Dropping tables...", flush=True)
        query.exec("DROP TABLE IF EXISTS customers")
        query.exec("DROP TABLE IF EXISTS stores")
        query.exec("DROP TABLE IF EXISTS orders")
        query.exec("DROP TABLE IF EXISTS products")
        query.exec("DROP TABLE IF EXISTS order_products")

        # create the tables
        # customers table
        print("Creating customers table...", flush=True)
        query.exec("""
            CREATE TABLE customers(
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                phone VARCHAR(25),
                email VARCHAR(255) NOT NULL
            )
        """)

        # stores table
        print("Creating stores table...", flush=True)
        query.exec("""
            CREATE TABLE stores(
                store_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                store_name VARCHAR(100) not null,
                phone VARCHAR(25),
                state VARCHAR(5)
            )
        """)

        # orders table
        # order_status: Pending = 1, Processing = 2, Completed = 3, Rejected = 4
        print("Creating orders table...", flush=True)
        query.exec("""
            CREATE TABLE orders(
                order_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                customer_id INTEGER,
                order_date TEXT NOT NULL,
                order_status TINYINT NOT NULL,
                store_id INTEGER NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (store_id) REFERENCES stores(store_id)
            )
        """)

        # products table
        print("Creating products table...", flush=True)
        query.exec("""
            CREATE TABLE products(
                product_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                product_name VARCHAR(100) NOT NULL,
                model_year VARCHAR(100) NOT NULL,
                list_price DECIMAL(10, 2) NOT NULL
            )
        """)

        # order_products table
        print("Creating order_products table...", flush=True)
        query.exec("""
            CREATE TABLE order_products(
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                list_price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)


class InsertDataIntoTables(QObject):
    def __init__(self, dbConn: QSqlDatabase, parent: QObject = None):
        super(InsertDataIntoTables, self).__init__(parent)
        self.conn = dbConn
        self.insertDataIntoTables()

    def insertDataIntoTables(self):
        """ populate tables created above """
        customers = [
            ["James", "Smith", 'NULL'],
            ["Mary", "Johnson", 'NULL'],
            ["John", "Williams", 'NULL'],
            ["Patricia", "Brown", '(716) 472-1234'],
            ["Lijing", "Ye", 'NULL'],
            ["Andrea", "Cotman", 'NULL'],
            ["Aaron", "Rountree", 'NULL'],
            ["Malik", "Ranger", 'NULL'],
            ["Helen", "Rodriguez", 'NULL'],
            ["Linda", "Martinez", 'NULL'],
            ["William", "Hernandez", '(757) 408-1121'],
            ["Elizabeth", "Lopez", '(804) 543-9876'],
            ["David", "Gonzalez", 'NULL'],
            ["Barbara", "Wilson", 'NULL'],
            ["Richard", "Anderson", 'NULL'],
            ["Susan", "Thomas", '(213) 854-7771'],
            ["Joseph", "Taylor", '(609) 341-9801'],
            ["Jessica", "Moore", '(707) 121-0909'],
            ["Thomas", "Jackson", 'NULL'],
            ["Sarah", "Martin", 'NULL'],
            ["Ryan", "Lee", 'NULL'],
            ["Cynthia", "Perez", '(754) 908-­5432'],
            ["Jacob", "Thompson", '(763) 765-1023'],
            ["Kathleen", "White", 'NULL'],
            ["Gary", "Harris", 'NULL'],
            ["Amy", "Sanchez", '(213) 198-4510'],
            ["Nicholas", "Clark", 'NULL'],
            ["Shirley", "Ramirez", '(231) 480-1567'],
            ["Eric", "Lewis", 'NULL'],
            ["Angela", "Miller", 'NULL']
        ]

        stores = [
            ['Boston Fish Supplies', '(617) 987-6543', 'MA'],
            ['Miami Fish Supplies', '(786) 123-4567', 'FL']
        ]

        products = [
            ['Orca Topwater Lure, 7 1/2"', 27.99, 2019],
            ['Feather Lure, 6"', 12.99, 2019],
            ['Sailure Fishing Lure, 5 1/2"', 24.99, 2020],
            ['Waxwing Saltwater Jig, 1/2 oz.', 13.99, 2020],
            ['7\'3" Bait-Stik Spinning Rod', 59.99, 2018],
            ['6\'6" Handcrafted Spinning Rod', 119.95, 2019],
            ['7\' Lite Spinning Rod', 169.99, 2020],
            ['7\' Boat Spinning Rod', 79.99, 2020],
            ['6\'6" Conventional Rod', 69.99, 2020],
            ['165 qt. Maxcold Cooler', 129.99, 2018],
            ['120 qt. Premium Marine Cooler', 399.99, 2019],
            ['5.3 Lever Drag Casting Reel', 199.99, 2018],
            ['4.6 Lever Drag Casting Reel', 249.99, 2020],
            ['Offshore Tackle Bag', 159.99, 2017]
        ]

        orders = [
            [2, '2020-01-04', 1, 1],
            [18, '2020-01-05', 2, 1],
            [30, '2020-01-08', 1, 2],
            [6, '2020-01-10', 3, 2],
            [21, '2020-01-11', 1, 2],
            [19, '2020-01-11', 3, 1],
            [27, '2020-01-12', 3, 1],
            [1, '2020-01-14', 2, 2],
            [5, '2020-01-15', 1, 2],
            [29, '2020-01-15', 2, 1],
            [28, '2020-01-16', 1, 2],
            [9, '2020-01-17', 1, 1],
            [26, '2020-01-17', 2, 2],
            [10, '2020-01-18', 3, 1],
            [3, '2020-01-18', 3, 2],
            [11, '2020-01-19', 4, 2],
            [14, '2020-01-20', 1, 1],
            [20, '2020-01-20', 2, 1],
            [8, '2020-01-20', 3, 1],
            [12, '2020-01-20', 2, 2],
            [15, '2020-01-21', 4, 1],
            [4, '2020-01-23', 1, 1],
            [22, '2020-01-24', 3, 2],
            [13, '2020-01-26', 2, 2],
            [7, '2020-01-26', 1, 2],
            [16, '2020-01-27', 3, 2],
            [17, '2020-01-29', 2, 1],
            [23, '2020-01-30', 3, 1],
            [24, '2020-02-01', 1, 2],
            [25, '2020-02-03', 2, 2]
        ]

        order_products = [
            [1, 2, 1, 24.99], [2, 14, 2, 159.99], [3, 11, 1, 399.99],
            [4, 1, 8, 27.99], [5, 1, 2, 12.99], [6, 4, 4, 13.99],
            [7, 1, 1, 27.99], [8, 8, 2, 79.99], [9, 8, 1, 79.99],
            [10, 13, 1, 249.99], [11, 1, 1, 27.99], [12, 11, 3, 399.99],
            [13, 12, 2, 199.99], [14, 7, 1, 169.99], [15, 3, 3, 24.99],
            [16, 10, 1, 129.99], [17, 13, 1, 249.99], [18, 6, 2, 119.95],
            [19, 5, 1, 59.99], [20, 8, 1, 79.99], [21, 6, 1, 119.95],
            [22, 5, 2, 59.99], [23, 14, 1, 159.99], [24, 2, 2, 12.99],
            [25, 1, 1, 27.99], [26, 10, 1, 129.99], [27, 2, 3, 12.99],
            [28, 9, 1, 69.99], [29, 13, 1, 249.99], [30, 6, 1, 119.95]
        ]

        query = QSqlQuery(self.conn)

        # create a prepared statement
        print("Populating customers table...", flush=True)
        query.prepare("""
            INSERT INTO customers (first_name, last_name, phone, email)
            VALUES (?, ?, ?, ?)
        """)
        for i in range(len(customers)):
            first_name = customers[i][0]
            last_name = customers[i][1]
            phone = customers[i][2]
            email = last_name.lower() + "." + first_name.lower() + "@email.com"
            query.addBindValue(first_name)
            query.addBindValue(last_name)
            query.addBindValue(phone)
            query.addBindValue(email)
            query.exec()

        print("Populating stores table...", flush=True)
        query.prepare("""
            INSERT INTO stores (store_name, phone, state)
            VALUES (?, ?, ?)
        """)
        for i in range(len(stores)):
            store_name = stores[i][0]
            phone = stores[i][1]
            state = stores[i][2]
            query.addBindValue(store_name)
            query.addBindValue(phone)
            query.addBindValue(state)
            query.exec()

        print("Populating products table...", flush=True)
        query.prepare("""
            INSERT INTO products (product_name, model_year, list_price)
            VALUES (?, ?, ?)
        """)
        for i in range(len(products)):
            product_name = products[i][0]
            list_price = products[i][1]
            model_year = products[i][2]
            query.addBindValue(product_name)
            query.addBindValue(model_year)
            query.addBindValue(list_price)
            query.exec()

        # orders table
        print("Populating orders table...", flush=True)
        query.prepare("""
            INSERT INTO orders (customer_id, order_date, order_status, store_id)
            VALUES (?, ?, ?, ?)
        """)
        for i in range(len(orders)):
            customer_id = orders[i][0]
            order_date = orders[i][1]
            order_status = orders[i][2]
            store_id = orders[i][3]
            query.addBindValue(customer_id)
            query.addBindValue(order_date)
            query.addBindValue(order_status)
            query.addBindValue(store_id)
            query.exec()

        # order_products table
        print("Populating order_products table...", flush=True)
        query.prepare("""
            INSERT INTO order_products (order_id, product_id, quantity, list_price)
            VALUES (?, ?, ?, ?)
        """)
        for i in range(len(order_products)):
            order_id = order_products[i][0]
            product_id = order_products[i][1]
            quantity = order_products[i][2]
            list_price = order_products[i][3]
            query.addBindValue(order_id)
            query.addBindValue(product_id)
            query.addBindValue(quantity)
            query.addBindValue(list_price)
            query.exec()


if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    conn: QSqlDatabase = None
    try:
        conn = connectToDatabase()
        if conn:
            CreateDatabaseObjects(conn)
            InsertDataIntoTables(conn)
    finally:
        if conn:
            conn.close()

    app.quit()
    # sys.exit(app.exec())
