// connect.cpp - connect to PostgreSQL using pqxx
// Tutorial at https://www.tutorialspoint.com/postgresql/postgresql_c_cpp.htm
//#include <fmt/core.h>
#include <iostream>
#include <pqxx/except>
#include <pqxx/pqxx>
#include <stdexcept>
#include <string>
#include <QCoreApplication>
#include <QFile>
#include <QSettings>

const QString getConnectionString()
{
  const QString config_file{"../config.cfg"};
  QFile file(config_file);
  if (!file.exists())
    //throw std::runtime_error("FATAL: could not find config file");
    throw std::runtime_error(
      std::format("FATAL: could not find config file {}. Cannot connect to database!",
        config_file.toStdString().c_str()));

  /*
   * program expects a database connection settings file named config.ini
   * in the the "current directory" from where this program runs
   * Format of config.ini is like an INI file & contains the following entries
   * NOTE: all names are case sensitive
   *
   * [postgres]
   * host=<<ip address of host>>
   * database=<<database name on host>>
   * user=<<login id>>
   * password=<<password>>
   */

  QSettings config("config.cfg", QSettings::IniFormat);
  QString host = config.value("postgres/host").toString();
  QString dbase = config.value("postgres/database").toString();
  QString user = config.value("postgres/user").toString();
  QString password = config.value("postgres/password").toString();

  QString connString = QString("hostaddr=%1 dbname=%2 user=%3 password=%4")
                         .arg(host, dbase, user, password);
  return connString;
}

int main(int argc, char **argv)
{
  QCoreApplication app(argc, argv);

  try {
    QString connStr = getConnectionString();
    pqxx::connection conn(connStr.toStdString().c_str());
    if (conn.is_open()) {
      std::cout << "Connected to database " << conn.dbname() << std::flush;
      // select query
      std::string sql("SELECT actor_id, first_name, last_name "
                      "FROM actor WHERE last_name "
                      "LIKE \'S%\'");
      // execute the query
      pqxx::work txn{conn};
      // query for a single value from database
      for (auto [version] : txn.stream<std::string_view>("SELECT version()")) {
        std::cout << " (PostgreSQL version " << version << ")" << std::endl;
      }
      std::cout << "Results of SQL: \'" << sql << "\'" << std::endl;
      // display the result
      for (auto [id, first_name, last_name] :
        txn.stream<int, std::string_view, std::string_view>(sql)) {
        std::string outstr = std::format("{:6d} {}, {}", id, last_name, first_name);
        std::cout << outstr << std::endl;
      }
      txn.commit();
    }
    else {
      std::cerr << "Can't open database dvdrental!" << std::endl;
      return -1;
    }
  }
  catch (pqxx::sql_error const &e) {
    std::cerr << "Database error: " << e.what() << std::endl
              << "Query was: " << e.query() << std::endl;
  }
  catch (const std::exception &e) {
    std::cerr << e.what() << std::endl;
    return -2;
  }
  return 0;
}
