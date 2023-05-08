# dbutils.py - database utility functions
import sys
import os
import psycopg2
from configparser import ConfigParser


def getConnectionParams(config_file_path, section="postgres"):
    """ get database connection params from config file"""
    parser = ConfigParser()
    assert os.path.exists(config_file_path), \
        f"FATAL: Configuration file {config_file_path} does not exist!"
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

def connect(config_file_path, section="postgres"):
    assert os.path.exists(config_file_path), \
        f"FATAL ERROR: {config_file_path} does not exist!"
    connection_params = getConnectionParams(config_file_path, section)
    conn = psycopg2.connect(**connection_params)
    return conn


