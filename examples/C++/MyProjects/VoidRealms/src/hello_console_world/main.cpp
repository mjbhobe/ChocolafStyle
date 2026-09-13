#include <QCoreApplication>
#include <QDebug>
#include <QList>
#include <QTextStream>
#include <QTimer>
#include <QtAlgorithms>
#include <format>
#include <string>
#include "test.h"

static QTextStream qcout(stdout);
static QTextStream qcerr(stderr);
static QTextStream qcin(stdin);

typedef QList<Test *> ListOfTest;

Test *createObject(QString objName, QObject *parent = nullptr)
{
  Test *obj = new Test(parent);
  obj->setObjectName(objName);
  return obj;
}

ListOfTest getList()
{
  // NOTE: QList is NOT a QObject, so copy is Ok!
  ListOfTest list;

  for (int i = 0; i < 5; ++i) {
    list.append(createObject("Test" + QString::number(i)));
  }
  return list;
}

void displayList(ListOfTest &list)
{
  // NOTE: I pass in a reference to avoid copying overhead!
  foreach (Test *obj, list) {
    qInfo() << obj;
  }
}

int main(int argc, char **argv)
{
  QCoreApplication app(argc, argv);
  std::string hello = std::format("Welcome to Qt {}", QT_VERSION_STR);

  // I can display QStrings to QTextStream
  qcout << QString::fromStdString(hello) << Qt::endl;

  // now I am going to create 3 new objects
  createObject("Pluto", &app);
  createObject("Daisy", &app);
  createObject("Petra", &app);
  createObject("Rocket", &app);

  ListOfTest list = getList();
  displayList(list);
  qDeleteAll(list);
  list.clear();

  QTimer timer;
  // fire only once after 3 secs & call app.quit
  timer.singleShot(3000, &app, &QCoreApplication::quit);

  auto ret = app.exec();
  qcout << "App quit with exit code " << ret << Qt::endl;

  return ret;
}
