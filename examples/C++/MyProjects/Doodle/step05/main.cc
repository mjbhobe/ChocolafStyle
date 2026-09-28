// ============================================================================
// main.cc: draw a single squiggle in the main window
//   click the left mouse & drag around the window to draw squiggle/doodle.
//
// Tutorial - Qt Scribble Application - Step05
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
//
// @author Manish Bhobé for Nämostuté Ltd.
// My experiments with C++,Qt, Python & PyQt.
// Code is provided for illustration purposes only! Use at your own risk.
// =============================================================================

#include <QApplication>
#include <QtGui>
#include "DrawWindow.h"
#include "chocolaf.h"
#include "constants.h"


int main(int argc, char **argv)
{
  // Chocolaf::ChocolafApp::setupForHighDpiScreens();
  // Chocolaf::ChocolafApp app(argc, argv);
  QApplication app(argc, argv);
  // app.setStyle("Fusion");
  app.setApplicationName(app.translate("main", AppTitle.toStdString().c_str()));

  // create the GUI
  DrawWindow mainWindow;
  Chocolaf::centerOnScreenWithSize(mainWindow, 0.75, 0.75);
  // mainWindow.resize(QGuiApplication::primaryScreen()->availableSize() * 4 /
  // 5);
  mainWindow.setWindowTitle(WindowTitle);
  mainWindow.show();

  return app.exec();
}
