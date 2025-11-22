// main.cpp - main driver program
//
#include <QApplication>
#include "mainWindow.h"

int main(int argc, char **argv) {
  QApplication app(argc, argv);

  MainWindow mainWindow;
  mainWindow.show();

  return app.exec();
}
