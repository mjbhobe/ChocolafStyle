// ============================================================================
// main.cc: Adding actions + menus + signals and slots
//
// Tutorial - Qt Scribble Application - Step08
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// Created by Manish Bhobé.
// ===========================================================================

#include <QApplication>
#include <QtGui>

#include "DrawWindow.h"
#include "chocolaf.h"
#include "constants.h"
#include "IconFont.h"


int main(int argc, char **argv)
{
  Chocolaf::ChocolafApp::setupForHighDpiScreens();
  QApplication app(argc, argv);

  app.setApplicationName(app.translate("main", AppTitle.toStdString().c_str()));

  // Initialize the icon font before creating any windows or actions
  IconFont::initFont();

  // create the GUI
  DrawWindow mainWindow;
  Chocolaf::centerOnScreenWithSize(mainWindow, 0.75, 0.75);
  mainWindow.setWindowTitle(WindowTitle);
  mainWindow.show();

  return app.exec();
}
