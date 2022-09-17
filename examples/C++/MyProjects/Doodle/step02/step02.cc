// ============================================================================
// step02.cc: Handling events in the main window with Qt's signals/slots
//
// Tutorial - Qt Scribble Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
//
// @author Manish Bhobe for Nämostuté Ltd.
// My experiments with C++,Qt, Python & PyQt.
// Code is provided for illustration purposes only! Use at your own risk.
// =============================================================================

#include "DrawWindow.h"
//#include "chocolaf.h"
#include <QApplication>
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

  app.setApplicationName(app.translate("main", "Qt Scribble"));

  // create the GUI
  DrawWindow mainWindow;
  mainWindow.show();

  return app.exec();
}
