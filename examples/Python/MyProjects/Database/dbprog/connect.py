from PyQt6.QtCore import *
from PyQt6.QtSql import *
from configparser import ConfigParser
import pathlib

def connect() -> QSqlDatabase:
    config_path = pathlib.Path(__file__).parent / "connect.ini"
    if config_path.exists():
        parser = ConfigParser()
        parser.read(str(config_path))
        # connection_params = {}
        section_name = "postgres_dvdrental"
        if parser.has_section(section_name):
#            params = parser.items(section)
#            for param in params:
#                connection_params[param[0]] = param[1]
#            db = QSqlDatabase("QPSQL")
#            db.setHostName(connection_params["host"])
#            db.setDatabaseName(connection_params["database"])
#            db.setUserName(connection_params["user_name"])
#            db.setPassword(connection_params["password"])
#            return db
            conn = QSqlDatabase.addDatabase("QPSQL", "postgres_dvdrental")
            conn.setHostName(parser.get(section_name, "host"))
            conn.setDatabaseName(parser.get(section_name, "database"))
            conn.setUserName(parser.get(section_name, "user_name"))
            conn.setPassword(parser.get(section_name, "password"))
            # connect
            conn.open()
            return conn
        else:
            raise IOError(f"Found {str(config_path)}! But it does not have a \'postgres_dvdrental\' entry!")
    else:
        raise OsError(f"Unable to locate {str(config_path)} to read db connection params!")
    

def main():
    app = QCoreApplication([])
    conn = connect()
    if not conn.isOpen():
        print("Unable to connect to database!")
        print(f"Last Error: {conn.lastError().text()}")
    else:
        query = QSqlQuery(conn)
        query.exec("select version() as version")
        while query.next():
            print(f"Using {query.value(0)}")
        print(f"Connected as {conn.userName()}@{conn.databaseName()}")
        prompt = f"{conn.userName()}@{conn.databaseName()} sql: "
        while True:
            query_str = input(prompt).strip()
            if query_str.lower() in ["exit", "quit"]:
                break
            if not query.exec(query_str):
                print("Coud not execute query")
                continue
            num_fields_selected = query.record().count()
            row_count = 0
            while query.next():
                row = ""
                for field_no in range(num_fields_selected):
                    row += str(query.value(field_no)) + "|"
                print(row)
                row_count += 1
            print(f"{row_count + 1} row(s) selected")


        



if __name__ == "__main__":
    main()


