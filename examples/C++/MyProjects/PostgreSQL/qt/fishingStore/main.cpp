// main.cpp - driving program
#include "FishingStoreSetupDb.h"
#include "chocolaf.h"
#include <QtCore>
#include <QtGui>
#include <QtSql>
#include <QtWidgets>
#include <fmt/core.h>
#include <iostream>
#include <pqxx/pqxx>
using namespace std;

QSqlDatabase connectToDatabase()
{
  QSqlDatabase db = QSqlDatabase::addDatabase("QPSQL");
  db.setHostName("localhost");
  db.setDatabaseName("fishingStore");
  db.setUserName("postgres");
  db.setPassword("M@ster$#");

  if (!db.open()) {
    cout << db.lastError().text().toStdString() << flush << endl;
    qFatal("Failed to connect to database!");
  }
  cout << "Connected to PostgreSQL db " << db.databaseName().toStdString() << endl
       << flush;
  return db;
}

const bool CREATE_DB_OBJECTS = true;
const bool INSERT_RECORDS = true;

int main(int argc, char **argv)
{
  QApplication app(argc, argv);
  //Chocolaf::ChocolafApp app(argc, argv);
  //app.setStyle("Chocolaf");

  // setup connection to database
  pqxx::connection conn(
    "hostaddr=127.0.0.1 dbname=fishingstore user=postgres password=M@st5r$"
  );
  if (!conn.is_open()) {
    cerr << "FATAL ERROR: unable to connect to database " << conn.dbname() << endl;
    return -1;
  }

  try {
    if (CREATE_DB_OBJECTS) {
      cout << "Creating database objects..." << endl;
      FishingStoreSetupDb::createDbObjects(conn);
    }
    if (INSERT_RECORDS) {
      cout << "Populating database..." << endl;
      FishingStoreSetupDb::populateDb(conn);
    }

    // setup Gui
    QWidget window;
    window.setWindowTitle("Fishing Store Example");
#if defined Q_OS_LINUX
    const std::string os{"Linux"};
#elif defined Q_OS_MACOS
    const std::string os{"MacOS"};
#else
    const std::string os{"Windows"};
#endif
    std::string winTitle = fmt::format(
      "Welcome to the QtFishingStore on {} using Qt {} for C++", os.c_str(), QT_VERSION_STR
    );
    QLabel *hello = new QLabel(winTitle.c_str());
    QVBoxLayout *layout = new QVBoxLayout();
    layout->addWidget(hello);
    window.setLayout(layout);
    window.show();
    return app.exec();
  }
  catch (const pqxx::sql_error &err) {
    cerr << "SQL Error: " << err.what() << endl;
    cerr << "Query was: " << err.query() << endl;
    return -1;
  }
  catch (const std::exception &err) {
    cerr << "Error: " << err.what() << endl;
    return -2;
  }
}
