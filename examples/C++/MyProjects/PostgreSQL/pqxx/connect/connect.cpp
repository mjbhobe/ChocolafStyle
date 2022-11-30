// connect.cpp - connect to PostgreSQL using pqxx
// Tutorial at https://www.tutorialspoint.com/postgresql/postgresql_c_cpp.htm
#include <fmt/core.h>
#include <iostream>
#include <pqxx/pqxx>
#include <string>
#include <QCoreApplication>
using namespace std;
using namespace pqxx;

int main(int argc, char **argv)
{
   QCoreApplication app(argc, argv);
   try {
      pqxx::connection conn(
         "hostaddr=127.0.0.1 dbname=dvdrental user=postgres password=M@ster$#");
      if (conn.is_open()) {
         cout << "Connected to database " << conn.dbname() << std::flush;
         // select query
         string sql("SELECT actor_id, first_name, last_name "
                    "FROM actor WHERE last_name "
                    "LIKE \'S%\'");
         // execute the query
         pqxx::work txn{conn};
         // query for a single value from database
         for (auto [version] : txn.stream<string_view>("SELECT version()")) {
            cout << " (PostgreSQL version " << version << ")" << endl;
         }
         //pqxx::result res{txn.exec(sql.c_str())};
         cout << "Results of SQL: \'" << sql << "\'" << endl;
         // display the result
         //for (auto row : res) {
         for (auto [id, first_name, last_name] :
              txn.stream<int, std::string_view, std::string_view>(sql)) {
            //int actor_id = row["actor_id"].as<int>();
            //std::string first_name = row["first_name"].as<string>();
            //std::string last_name = row["last_name"].as<string>();
            //std::printf("%6d: %s, %s\n", actor_id, first_name.c_str(), last_name.c_str());
            std::string outstr = fmt::format("{:6d} {}, {}", id, last_name, first_name);
            //                                             row["actor_id"].as<int>(),
            //                                             row["last_name"].as<string>(),
            //                                             row["first_name"].as<string>());
            cout << outstr << endl;
         }
         txn.commit();
      }
      else {
         cerr << "Can't open database dvdrental!" << endl;
         return -1;
      }
   }
   catch (const std::exception &e) {
      cerr << e.what() << endl;
      return -2;
   }
   return 0;
}
