// connect.cpp - connect to PostgreSQL using QtSQL
#include <fmt/core.h>
#include <iostream>
#include <QtCore>
#include <QtSql>
using namespace std;

int main(int argc, char **argv)
{
   QCoreApplication app(argc, argv);

   // setup PostgreSQL database
   QSqlDatabase db = QSqlDatabase::addDatabase("QPSQL");
   db.setHostName("localhost");
   db.setDatabaseName("dvdrental");
   db.setUserName("postgres");
   db.setPassword("M@ster$#");
   if (!db.open()) {
      cout << db.lastError().text().toStdString() << flush << endl;
      qFatal("Failed to connect to database!");
   }
   else {
      cout << "Connected to PostgreSQL db " << db.databaseName().toStdString() << endl
           << flush;
      QString sql("SELECT actor_id, first_name, last_name "
                  "FROM actor WHERE last_name "
                  "LIKE \'S%\'");
      QSqlQuery query(db);
      if (!query.exec(sql)) {
         //cerr << db.lastError().text().toStdString() << flush << endl;
         fmt::print("Query failed! Query {} - Error {}\n", sql.toStdString(),
                    query.lastError().text().toStdString());
      }
      else {
         cout << "Executing \'" << sql.toStdString() << "\'" << endl;
         while (query.next()) {
            /*
            int actor_id = query.value("actor_id").toInt();
            const string first_name = query.value("first_name").toString().toStdString();
            const string last_name = query.value("last_name").toString().toStdString();

            //cout << fmt::format("{:.6d} {}, {}\n", actor_id, last_name, first_name);
            cout << actor_id << " " << last_name << ", " << first_name << endl;
            */
            QString row = QString("%1 %2, %3")
                             .arg(query.value("actor_id").toInt(), 6)
                             .arg(query.value("last_name").toString())
                             .arg(query.value("first_name").toString());
            cout << row.toStdString() << endl;
         }
      }
   }
   db.close();
   return 0;
}
