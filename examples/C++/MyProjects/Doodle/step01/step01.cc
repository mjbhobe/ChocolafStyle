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
#include "chocolaf.h"
#include <QApplication>
#include <QMainWindow>
#include <QtGui>

int main(int argc, char **argv)
{
  QApplication app(argc, argv);
  // use Chocolaf style
  QFile f(":chocolaf/chocolaf.css");
  if (!f.exists()) {
    printf("Unable to open stylesheet!");
  } else {
    f.open(QFile::ReadOnly | QFile::Text);
    QTextStream ts(&f);
    app.setStyleSheet(ts.readAll());
  }

  // create the GUI
  QMainWindow mainWindow;
  QString title =
      QString("Qt %1 Doodle with Chocolaf - Step01: Basic Window").arg(QT_VERSION_STR);
  mainWindow.setWindowTitle(title);
  mainWindow.resize(QGuiApplication::primaryScreen()->availableSize() * 4 / 5);
  mainWindow.show();

  return app.exec();
}
