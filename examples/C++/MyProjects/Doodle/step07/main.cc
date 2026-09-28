// ============================================================================
// main.cc: Adding collection of lines to doodle + loading & saving lines
//
// Tutorial - Qt Scribble Application - Step07
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// Created by Manish Bhobé.
// ===========================================================================

#include "DrawWindow.h"
#include "chocolaf.h"
#include <QApplication>
#include <QtGui>
#include "constants.h"

int main(int argc, char** argv)
{
  Chocolaf::ChocolafApp::setupForHighDpiScreens();
  //Chocolaf::ChocolafApp app(argc, argv);
  QApplication app(argc, argv);
  app.setStyle("Fusion");
  app.setApplicationName(app.translate("main", AppTitle.toStdString().c_str()));

  // create the GUI
  DrawWindow mainWindow;
  Chocolaf::centerOnScreenWithSize(mainWindow, 1.75, 0.65);
  mainWindow.setWindowTitle(WindowTitle);
  mainWindow.show();

  return app.exec();
}
