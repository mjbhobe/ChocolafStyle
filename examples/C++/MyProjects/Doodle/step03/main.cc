// ============================================================================
// main.cc: Handling events in the main window with Qt's signals/slots
//
// Tutorial - Qt Scribble Application - Step03
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
//
// @author Manish Bhobé for Nämostuté Ltd.
// My experiments with C++,Qt, Python & PyQt.
// Code is provided for illustration purposes only! Use at your own risk.
// =============================================================================

#include "DrawWindow.h"
#include "chocolaf.h"
#include <QApplication>
#include <QTextStream>
#include <QtGui>

QTextStream cout(stdout, QIODeviceBase::WriteOnly);
const QString title = QString("Qt %1 Scribble - Step03: Handling Events").arg(QT_VERSION_STR);

int main(int argc, char **argv) {
  QApplication app(argc, argv);

  app.setApplicationName(app.translate("main", "Qt Scribble"));

  // create the GUI
  DrawWidget mainWindow;
  mainWindow.setWindowTitle(title);
  Chocolaf::centerOnScreenWithSize(mainWindow, 0.75, 0.75);
  mainWindow.show();

  return app.exec();
}
