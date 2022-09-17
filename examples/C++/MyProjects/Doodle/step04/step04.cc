// ============================================================================
// step01.cc: draw a single squiggle in the main window
//   click the left mouse & drag around the window to draw squiggle/doodle.
//
// Tutorial - Qt Scribble Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
//
// @author Manish Bhobe for Nämostuté Ltd.
// My experiments with C++,Qt, Python & PyQt.
// Code is provided for illustration purposes only! Use at your own risk.
// =============================================================================

#include "DrawWindow.h"
#include <QApplication>
#include <QtGui>

const QString AppTitle("Qt Scribble");

int main(int argc, char **argv)
{
   QApplication app(argc, argv);

   QFile f(":chocolaf/chocolaf.css");

   if (!f.exists()) {
      printf("Unable to open stylesheet!");
   } else {
      f.open(QFile::ReadOnly | QFile::Text);
      QTextStream ts(&f);
      app.setStyleSheet(ts.readAll());
   }
   app.setApplicationName(app.translate("main", AppTitle.toStdString().c_str()));

   // create the GUI
   DrawWindow mainWindow;
   mainWindow.resize(QGuiApplication::primaryScreen()->availableSize() * 4 / 5);
   mainWindow.show();

   return app.exec();
}
