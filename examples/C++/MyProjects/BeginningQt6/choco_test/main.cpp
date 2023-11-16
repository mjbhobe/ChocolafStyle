#include "chocolaf.h"
#include "mainwindow.h"

#include <QApplication>

int main(int argc, char *argv[]) {
  QApplication app(argc, argv);
  // Chocolaf::ChocolafApp app(argc, argv);
  // app.setStyle("Chocolaf");
  Chocolaf::setChocolafStyle(app, "Chocolaf");

  MainWindow w;
  w.show();

  return app.exec();
}
