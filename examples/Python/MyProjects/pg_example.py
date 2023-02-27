""" pg_example.py - connect to PostgreSQL database """
import sys
import pathlib
import psycopg2
from configparser import ConfigParser


def get_db_params(config_file = "database.ini", section = "postgresql_suppliers"):
    parser = ConfigParser()
    config_file_path = pathlib.Path(__file__).parents[0].joinpath(config_file)
    db_params = {}

    if not config_file_path.exists():
        raise RuntimeError(f"Unable to locate config file {config_file}")
    else:
        parser.read(config_file_path)

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise RuntimeError(f"{config_file} does not have {section} section!")

    return db_params


def get_connection(test = False):
    """ connect to PostgreSQL database """
    conn = None
    try:
        db_params = get_db_params()
        print("Connecting to database....")
        conn = psycopg2.connect(**db_params)

        if test:
            cur = conn.cursor()
            cur.execute("SELECT version()")
            db_version = cur.fetchone()[0]
            print(f"Connected to {db_version}")
            cur.close()

        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def create_tables():
    """ create tables in the PostgreSQL database """
    commands = (
        """
            create table vendors(
                vendor_id serial primary key,
                vendor_name varchar(255) not null
            )
        """,
        """
            create table parts(
                part_id serial primary key,
                part_name varchar(255) not null
            )
        """,
        """
            create table drawings(
                part_id integer primary key,
                file_extension varchar(5) not null,
                drawing_data bytea not null,
                foreign key (part_id)
                    references parts (part_id)
                    on update cascade on delete cascade
            )
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
        """
    )

    conn = None
    try:
        conn = get_connection(True)
        cur = conn.cursor()
        # cycle through all the DDL commands
        for command in commands:
            print(command)
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_vendor(vendor_name):
    """ insert rows into vendors table """
    sql = """insert into vendors(vendor_name) 
             values(%s) returning vendor_id;"""
    conn = None
    try:
        conn = get_connection(True)
        cur = conn.cursor()
        cur.execute(sql, (vendor_name,))
        # get the vendor id generated
        vendor_id = cur.fetchone()[0]
        print(f"{vendor_name} inserted")
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_vendor_list(vendor_list):
    """ insert multiple vendors into vendors table """
    sql = """insert into vendors(vendor_name) values(%s)"""
    conn = None
    try:
        conn = get_connection(True)
        cur = conn.cursor()
        cur.executemany(sql, vendor_list)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def main():
    # db_params = get_db_params()
    # create_tables()
    # insert_vendor("3M Co.")
    insert_vendor_list(
        [
            ('AKM Semiconductor Inc.',),
            ('Asahi Glass Co Ltd.',),
            ('Daikin Industries Ltd.',),
            ('Dynacast International Inc.',),
            ('Foster Electric Co. Ltd.',),
            ('Murata Manufacturing Co. Ltd.',)
        ]
    )


if __name__ == "__main__":
    main()
