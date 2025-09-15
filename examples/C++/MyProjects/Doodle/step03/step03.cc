// ============================================================================
// step03.cc: Drawing in the main window - the point where the left mouse
//   is clicked is shown in the window
//
// Tutorial - Qt Scribble Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
//
// @author Manish Bhobé for Nämostuté Ltd.
// My experiments with C++,Qt, Python & PyQt.
// Code is provided for illustration purposes only! Use at your own risk.
// =============================================================================
#include <QApplication>
#include <QMainWindow>
#include <QMessageBox>
#include <QtGui>

#include "DrawWindow.h"
#include "chocolaf.h"

const QString AppTitle("Qt Scribble");
const QString WinTitle = QString("Qt %1 Doodle - Step03: Handling mouse clicks")
                             .arg(QT_VERSION_STR);

int main(int argc, char **argv)
{
  QApplication app(argc, argv);
  //Chocolaf::setChocolafStyle(app, "WindowsDark");

  app.setApplicationName(app.translate("main", AppTitle.toStdString().c_str()));

  // create the GUI
  DrawWindow *drawWidget = new DrawWindow;
  DrawMainWindow mainWindow(drawWidget);
  mainWindow.setWindowTitle(WinTitle);
  mainWindow.setCentralWidget(drawWidget);
  Chocolaf::centerOnScreenWithSize(mainWindow, 0.75, 0.75);
  mainWindow.show();

  return app.exec();
}
