#include <QtCore>
#include <QTextStream>

int main(int argc, char **argv)
{
  QCoreApplication app(argc, argv);
  QTextStream cout(stdout);

  cout << QString("Hello! Welcome to Qt programming.\nYou are using Qt %1").arg(QT_VERSION_STR);
  return EXIT_SUCCESS;
}
