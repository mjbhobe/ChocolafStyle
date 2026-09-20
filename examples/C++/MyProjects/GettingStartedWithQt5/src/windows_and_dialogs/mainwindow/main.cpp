#include <QApplication>

#include <format>
#include "mainwindow.h"

int main(int argc, char **argv)
{
  QApplication app(argc, argv);

  MainWindow mainWin;
  std::string title = std::format("Qt{} | QFrameWindow", QT_VERSION_STR);
  mainWin.setWindowTitle(QString::fromStdString(title));
  mainWin.resize(640, 480);
  mainWin.show();

  return app.exec();
}
