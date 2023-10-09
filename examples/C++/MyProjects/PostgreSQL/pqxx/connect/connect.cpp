// connect.cpp - connect to PostgreSQL using pqxx
// Tutorial at https://www.tutorialspoint.com/postgresql/postgresql_c_cpp.htm
#include <QCoreApplication>
#include <QFile>
#include <QSettings>
#include <fmt/core.h>
#include <iostream>
#include <pqxx/pqxx>
#include <string>
using namespace std;
using namespace pqxx;

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

    QString connString = QString("hostaddr=%1 dbname=%2 user=%3 password=%4")
                             .arg(host, dbase, user, password);
    return connString;
}

int main(int argc, char** argv)
{
    QCoreApplication app(argc, argv);

    try {
        QString connStr = getConnectionString();
        pqxx::connection conn(connStr.toStdString().c_str());
        // "hostaddr=127.0.0.1 dbname=dvdrental user=postgres password=M@ster$#");
        if (conn.is_open()) {
            cout << "Connected to database " << conn.dbname() << std::flush;
            // select query
            string sql("SELECT actor_id, first_name, last_name "
                       "FROM actor WHERE last_name "
                       "LIKE \'S%\'");
            // execute the query
            pqxx::work txn { conn };
            // query for a single value from database
            for (auto [version] : txn.stream<string_view>("SELECT version()")) {
                cout << " (PostgreSQL version " << version << ")" << endl;
            }
            cout << "Results of SQL: \'" << sql << "\'" << endl;
            // display the result
            // pqxx::result res{txn.exec(sql.c_str())};
            // for (auto row : res) {
            for (auto [id, first_name, last_name] :
                txn.stream<int, std::string_view, std::string_view>(sql)) {
                // int actor_id = row["actor_id"].as<int>();
                // std::string first_name = row["first_name"].as<string>();
                // std::string last_name = row["last_name"].as<string>();
                // std::printf("%6d: %s, %s\n", actor_id, first_name.c_str(), last_name.c_str());
                std::string outstr = fmt::format("{:6d} {}, {}", id, last_name, first_name);
                cout << outstr << endl;
            }
            txn.commit();
        } else {
            cerr << "Can't open database dvdrental!" << endl;
            return -1;
        }
    } catch (const std::exception& e) {
        cerr << e.what() << endl;
        return -2;
    }
    return 0;
}
