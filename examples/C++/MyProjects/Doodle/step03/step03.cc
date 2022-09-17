// ============================================================================
// step03.cc: Drawing in the main window - the point where the left mouse
//   is clicked is shown in the window
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
#include <QMainWindow>
#include <QMessageBox>
#include <QtGui>

const QString AppTitle("Qt Scribble");
const QString WinTitle = QString("Qt %1 Doodle - Step03: Handling mouse clicks").arg(QT_VERSION_STR);

void DrawMainWindow::closeEvent(QCloseEvent *event)
{
   // window is about to close, prompt user & decide
   // if ok to quit based on user's response.
   qDebug() << "DrawMainWindow::closeEvent() called. _modified = "
            << (_drawWindow->isModified() ? "True" : "False");

   if (_drawWindow->isModified()) {
      switch (
         QMessageBox::question(this, tr("Qt Scribble Tutorial"),
                               tr("Contents of the doodle have changed.\nDo you want to quit without saving?"),
                               QMessageBox::Yes | QMessageBox::No, QMessageBox::No)) {
         case QMessageBox::Yes:
            // ok to quit
            qDebug() << "User chose to quit without saving...";
            event->accept();
            break;
         default:
            // don't quit yet
            event->ignore();
      }
   } else {
      event->accept();
   }
}

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
   DrawWindow *drawWidget = new DrawWindow;
   DrawMainWindow mainWindow(drawWidget);
   mainWindow.setWindowTitle(WinTitle);
   mainWindow.setCentralWidget(drawWidget);
   mainWindow.resize(QGuiApplication::primaryScreen()->availableSize() * 4 / 5);
   mainWindow.show();

   return app.exec();
}
