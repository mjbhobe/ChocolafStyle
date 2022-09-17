// ============================================================================
// step05.cc: ability to set the squiggle's thickness & color
//  - Ctrl+left mouse click - set squiggle's thickness
//  - Ctrl+right mouse click - set squiggle's color
//  (NOTE: this is an absolutely ridiculous GUI design!! Purpose of this code
//   is not to present a good GUI design yet! This flaw will be corrected in
//   further step(s) when menus & toolbars will be introduced)
//
// Tutorial - Qt Scribble Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
//
// @author Manish Bhobe for Nämostuté Ltd.
// My experiments with C++,Qt,Python & PyQt.
// Code is provided for illustration purposes only! Use at your own risk.
// =============================================================================

#include "DrawWindow.h"
#include "chocolaf.h"
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
