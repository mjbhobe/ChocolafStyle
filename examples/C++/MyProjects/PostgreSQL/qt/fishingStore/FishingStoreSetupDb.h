#ifndef FISHINGSTORESETUPDB_H
#define FISHINGSTORESETUPDB_H

#include <QObject>
#include <pqxx/pqxx>

class FishingStoreSetupDb : public QObject
{
  Q_OBJECT
public:
  static void createDbObjects(pqxx::connection &conn);
  static void populateDb(pqxx::connection &conn);

protected:
  static void dropTables(pqxx::connection &conn);
  static void createTables(pqxx::connection &conn);

signals:
};

#endif // FISHINGSTORESETUPDB_H
