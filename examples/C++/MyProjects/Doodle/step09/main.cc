// ============================================================================
// main.cc: Loading & saving collection of lines
//
// Tutorial - Qt Scribble Application - Step 09
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// Created by Manish Bhobé.
// ===========================================================================

#include <QApplication>
#include <QtGui>

#include "MainWindow.h"
#include "chocolaf.h"
#include "constants.h"
#include "IconFont.h"

//const QString AppTitle("Qt Scribble");

int main(int argc, char **argv)
{
   Chocolaf::ChocolafApp::setupForHighDpiScreens();
   QApplication app(argc, argv);
   //Chocolaf::setChocolafStyle(app, "Chocolaf");

   app.setApplicationName(app.translate("main", AppTitle.toStdString().c_str()));

   // Initialize the icon font before creating any windows or actions
   IconFont::initFont();

   // create the GUI
   MainWindow mainWindow;
   Chocolaf::centerOnScreenWithSize(mainWindow, 0.75, 0.75);
   mainWindow.setWindowTitle(WindowTitle);
   mainWindow.show();

   return app.exec();
}
