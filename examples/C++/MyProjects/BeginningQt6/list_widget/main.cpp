// main.cpp: main driver program
#include "chocolaf.h"
#include "list_widget.h"
#include <QApplication>
#include <fmt/core.h>

int main(int argc, char **argv) {
  QApplication app(argc, argv);
  Chocolaf::setChocolafStyle(app, "Fusion");

  MainWidget widget;
  widget.setWindowTitle(
      fmt::format("Qt{} list widget example", QT_VERSION_STR).c_str());
  widget.show();

  return app.exec();
}
