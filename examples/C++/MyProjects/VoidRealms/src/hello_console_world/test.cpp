#include "test.h"
#include <QDebug>
#include <QObject>


Test::Test(QObject *parent) : QObject(parent)
{
  qInfo() << "Object constructed";
}

Test::~Test() { qInfo() << this << ": object destructed!"; }
