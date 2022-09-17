// ============================================================================
// step08.cc: Adding toolbar & status bar
//
// Tutorial - Qt Scribble Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// Created by Manish Bhobe.
// ===========================================================================

#include "MainWindow.h"
#include <QApplication>
#include <QDebug>
#include <QStyleFactory>
#include <QtGui>

static MainWindow *__pMainWindow = nullptr;

MainWindow *getMainWindow()
{
   // it is assumed that this will always be a  valid ptr
   // from all points where it is called from. Hence the assert
   Q_ASSERT(__pMainWindow != nullptr);
   return __pMainWindow;
}

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
   MainWindow *mainWindow = new MainWindow();
   __pMainWindow = mainWindow;
   mainWindow->show();

   int ret = app.exec();
   delete mainWindow;
   return ret;
}
