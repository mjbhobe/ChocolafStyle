// ==================================================================================
// Hello World - basic Qt Console Application
//
// @author: Manish Bhobe
// My Experiments with C/C++, Qt Framework and STL
// Code shared for learning purposes only. Use at your own risk!
// ==================================================================================
#include <QCoreApplication>
#include <QDebug>
#include <format>
#include <string>

int main(int argc, char** argv)
{
  QCoreApplication app(argc, argv);

  std::string hello = std::format("Hello Qt {} World!", QT_VERSION_STR);
  qInfo() << QString::fromStdString(hello);

  return app.exec();
}
