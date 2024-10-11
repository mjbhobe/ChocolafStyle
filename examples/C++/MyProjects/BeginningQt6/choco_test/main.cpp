#include "chocolaf.h"
#include "mainwindow.h"
#include <format>

#include <QApplication>

int main(int argc, char *argv[]) {
  QApplication app(argc, argv);
  // Chocolaf::ChocolafApp app(argc, argv);
  // app.setStyle("Chocolaf");
  Chocolaf::setChocolafStyle(app, "Chocolaf");

  MainWindow w;
  w.setWindowTitle(std::format("Welcome to Qt {}", QT_VERSION_STR).c_str());
  w.show();

  return app.exec();
}
