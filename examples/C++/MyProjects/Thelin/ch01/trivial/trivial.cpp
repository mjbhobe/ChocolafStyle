// trivial.cpp: trivial C++ program with Qt
//#include "chocolaf.h"
#include <QtCore>
#include <format>
//#include <fmt/format.h>
#include <QDebug>

static QTextStream cout(stdout, QIODeviceBase::WriteOnly);

int main(int /*argc*/, char ** /*argv*/)
{
   qDebug() << "Hello Qt " << QT_VERSION_STR << " World!" << Qt::endl;
   qDebug() << std::format("std::format -> Hello Qt {} World!\n", QT_VERSION_STR).c_str();
   return 0;
}
