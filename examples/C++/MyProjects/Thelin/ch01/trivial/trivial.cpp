// trivial.cpp: trivial C++ program with Qt
#include <QString>
#include <QTextStream>
#include <format>

// NOTE: don't include <iostream>!!

static QTextStream cout(stdout, QIODeviceBase::WriteOnly);

int main(int /*argc*/, char ** /*argv*/)
{
  cout << "Hello Qt " << QT_VERSION_STR << " World!" << Qt::endl;
  // NOTE: cout is QTextStream, which does not support std::string,
  // However, it supports const char*, hence the c_str()
  cout << std::format("std::format -> Hello Qt {} World!\n", QT_VERSION_STR).c_str();
  // using QString native formatting
  cout << QString("QString::arg -> Hello Qt %1 World!").arg(QT_VERSION_STR) << Qt::endl;
  cout << QString::fromStdString(
      std::format("QString::fromStdString -> Hello Qt {} World!\n", QT_VERSION_STR));
  return 0;
}
