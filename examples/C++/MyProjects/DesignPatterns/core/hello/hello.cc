// hello.cc - Hello Qt
#include <QtCore>
#include <cstdlib>

// NOTE: DO NOT include <iostream> header!!
static QTextStream cout(stdout, QIODevice::WriteOnly);

int main(int argc, char **argv) {
  QCoreApplication app(argc, argv);

  cout << "Hello World! Welcome to Qt " << QT_VERSION_STR << Qt::endl;

  return EXIT_SUCCESS;
}
