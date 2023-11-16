// ============================================================================
// step01.cc: Creating a basic application with Qt/C++
//
// Tutorial - Qt Scribble Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
//
// @author Manish Bhobe for Nämostuté Ltd.
// My experiments with C++,Qt, Python & PyQt.
// Code is provided for illustration purposes only! Use at your own risk.
// =============================================================================
#include <QApplication>
#include <QMainWindow>
#include <QtGui>

#include "chocolaf.h"

int main(int argc, char **argv) {
  QApplication app(argc, argv);
  Chocolaf::setChocolafStyle(app, "Chocolaf");

  // create the GUI
  QMainWindow mainWindow;
  QString title = QString("Qt %1 Doodle with Chocolaf - Step01: Basic Window")
                      .arg(QT_VERSION_STR);
  mainWindow.setWindowTitle(title);
  Chocolaf::centerOnScreenWithSize(mainWindow, 0.75, 0.75);
  mainWindow.show();

  return app.exec();
}
