# create_database.py - create a new PostgreSQL database
# and populate it with data
import sys
import os
import pathlib
from dbutils import connect
import psycopg2
from typing import Union


def createTables(conn):
    """create tables in the new database"""
    commands = (
        """
        DROP TABLE IF EXISTS vendors CASCADE;
        """,
        """
        CREATE TABLE vendors(
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """
        DROP TABLE IF EXISTS parts CASCADE;
        """,
        """ 
        CREATE TABLE parts (
            part_id SERIAL PRIMARY KEY,
            part_name VARCHAR(255) NOT NULL
        )
        """,
        """
        DROP TABLE IF EXISTS part_drawings CASCADE;
        """,
        """
        CREATE TABLE part_drawings (
            part_id INTEGER PRIMARY KEY,
            file_extension VARCHAR(5) NOT NULL,
            drawing_data BYTEA NOT NULL,
            FOREIGN KEY (part_id)
            REFERENCES parts (part_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        DROP TABLE IF EXISTS vendor_parts CASCADE;
        """,
        """
        CREATE TABLE vendor_parts (
            vendor_id INTEGER NOT NULL,
            part_id INTEGER NOT NULL,
            PRIMARY KEY (vendor_id , part_id),
            FOREIGN KEY (vendor_id)
                REFERENCES vendors (vendor_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
    )
    assert (
        conn is not None
    ), f"FATAL: createTables() requires valid database connection!"
    cursor = None
    try:
        cursor = conn.cursor()
        for command in commands:
            print(f"Executing {command}...", flush=True)
            cursor.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        conn.commit()


def insertVendors(conn, vendor_name_or_list: Union[str, list]):
    """populate tables created in function above"""
    sql = """
        INSERT INTO vendors(vendor_name)
        VALUES(%s)
        """
    if type(vendor_name_or_list) is str:
        sql = sql + " RETURNING vendor_id"
    sql = sql + ";"
    assert (
        conn is not None
    ), f"FATAL: insertVendor() requires valid database connection!"
    cursor = None
    try:
        # create a cursor
        cursor = conn.cursor()
        # execute a single SQL
        if type(vendor_name_or_list) is str:
            cursor.execute(
                sql,
                [
                    vendor_name_or_list,
                ],
            )
            # get inserted vendor_id
            vendor_id = cursor.fetchone()[0]
            print(
                f"insertVendor(): Inserted vendor {vendor_name_or_list} with id {vendor_id}"
            )
        else:
            cursor.executemany(sql, vendor_name_or_list)
            print(
                f"insertVendor(): Inserted {len(vendor_name_or_list)} vendors into db"
            )
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"ERROR in insertVendor() -> {error}")
    finally:
        if cursor is not None:
            cursor.close()
        conn.commit()


def main():
    try:
        # connect to database
        config_file_path = pathlib.Path(__file__).parent / "connect.ini"
        conn = connect(config_file_path, "postgres_vendors")
        curr = conn.cursor()
        curr.execute("SELECT current_database()")
        print(f"Connected to PostgreSQL database {curr.fetchone()}.")
        # create the tables
        createTables(conn)
        # insert a single vendor
        insertVendors(conn, "3M Co.")
        # insert multiple vendors
        insertVendors(
            conn,
            [
                ("AKM Semiconductor Inc.",),
                ("Asahi Glass Co Ltd.",),
                ("Daikin Industries Ltd.",),
                ("Dynacast International Inc.",),
                ("Foster Electric Co. Ltd.",),
                ("Murata Manufacturing Co. Ltd.",),
            ],
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
