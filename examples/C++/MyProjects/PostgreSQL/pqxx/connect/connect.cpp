// connect.cpp - connect to PostgreSQL using pqxx
// Tutorial at https://www.tutorialspoint.com/postgresql/postgresql_c_cpp.htm
#include <QCoreApplication>
#include <QFile>
#include <QSettings>
#include <fmt/core.h>
#include <iostream>
#include <pqxx/pqxx>
#include <string>
// using namespace std;
// using namespace pqxx;

const QString getConnectionString()
{
    QFile file("config.ini");
    if (!file.exists())
        throw QString("FATAL: could not find config file %1").arg("config.ini");

    QSettings config("config.ini", QSettings::IniFormat);
    QString host = config.value("Postgres/host").toString();
    QString dbase = config.value("Postgres/database").toString();
    QString user = config.value("Postgres/user").toString();
    QString password = config.value("Postgres/password").toString();

    // "hostaddr=127.0.0.1 dbname=dvdrental user=postgres password=M@ster$#");
    QString connString = QString("hostaddr=%1 dbname=%2 user=%3 password=%4")
                             .arg(host, dbase, user, password);
    return connString;
}

int main(int argc, char** argv)
{
    QCoreApplication app(argc, argv);

    try {
        QString connStr = getConnectionString();
        // pqxx::connection conn("hostaddr=127.0.0.1 dbname=dvdrental user=postgres password=M@ster$#");
        pqxx::connection conn(connStr.toStdString().c_str());
        if (conn.is_open()) {
            std::cout << "Connected to database " << conn.dbname() << std::flush;
            // select query
            std::string sql("SELECT actor_id, first_name, last_name "
                            "FROM actor WHERE last_name "
                            "LIKE \'S%\'");
            // execute the query
            pqxx::work txn { conn };
            // query for a single value from database
            for (auto [version] : txn.stream<std::string_view>("SELECT version()")) {
                std::cout << " (PostgreSQL version " << version << ")" << std::endl;
            }
            std::cout << "Results of SQL: \'" << sql << "\'" << std::endl;
            // display the result
            /* this is one way to display the results
            pqxx::result res{txn.exec(sql.c_str())};
            for (auto row : res) {
                int actor_id = row["actor_id"].as<int>();
                std::string first_name = row["first_name"].as<string>();
                std::string last_name = row["last_name"].as<string>();
                std::printf("%6d: %s, %s\n", actor_id, first_name.c_str(), last_name.c_str());
            } */
            // this is a succinct way
            for (auto [id, first_name, last_name] :
                txn.stream<int, std::string_view, std::string_view>(sql)) {
                std::string outstr = fmt::format("{:6d} {}, {}", id, last_name, first_name);
                std::cout << outstr << std::endl;
            }
            txn.commit();
        } else {
            std::cerr << "Can't open database dvdrental!" << std::endl;
            return -1;
        }
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return -2;
    }
    return 0;
}
