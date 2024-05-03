# connect.py - connect to the dvdrental database
import os
import psycopg2
import pathlib
from configparser import ConfigParser


def connect1():
    # this is a very very bad practice!
    # NEVER EMBED connection strings into code
    connect_str = "host=localhost dbname=dvdrental user=postgres password=M@ster$#"
    conn = psycopg2.connect(connect_str)
    return conn


def connect2():
    # an alternate form - still bad as we are embedding
    # connection strings into our code directly
    connect_params = dict(
        host="localhost",
        database="dvdrental",
        user="postgres",
        # and password if set
        password="M@ster$#",
    )
    conn = psycopg2.connect(**connect_params)
    return conn


def getConfigParams(config_file_path, section):
    parser = ConfigParser()
    assert os.path.exists(
        config_file_path
    ), f"FATAL: Configuration file {config_file_path} does not exist!"
    parser.read(config_file_path)

    # read params from section
    connect_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            connect_params[param[0]] = param[1]
    else:
        raise ValueError(f"FATAL: {config_file_path} does not have section {section}!")

    return connect_params


def connect3():
    """this is a good method, connection params are read
    from a configuration file.
    Create a configuration file with ini extension in same
    folder where this file is saved - see config.ini for
    example
    """
    config_file_path = pathlib.Path(__file__).parent / "connect.ini"
    connect_params = getConfigParams(config_file_path, "postgres")
    conn = psycopg2.connect(**connect_params)
    return conn


def main():
    try:
        conn1 = connect1()
        curr1 = conn1.cursor()
        curr1.execute("select version()")
        print(f"#1 > connected to PostgreSQL {curr1.fetchone()}")

        conn2 = connect2()
        curr2 = conn2.cursor()
        curr2.execute("select version()")
        print(f"#2 > connected to PostgreSQL {curr2.fetchone()}")

        conn3 = connect3()
        curr3 = conn3.cursor()
        curr3.execute("select version()")
        print(f"#3 > connected to PostgreSQL {curr3.fetchone()}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # close all opened connections
        if conn1 is not None:
            conn1.close()
        if conn2 is not None:
            conn2.close()
        if conn3 is not None:
            conn3.close()


if __name__ == "__main__":
    main()
