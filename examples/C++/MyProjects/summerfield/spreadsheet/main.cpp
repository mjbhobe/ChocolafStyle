#include "chocolaf.h"
#include <QApplication>
#include <QFile>
#include <QTextStream>

//#include "chocolaf.h"
#include "mainwindow.h"

const QString AppTitle("Qt with OpenCV ImageEditor");

int main(int argc, char **argv)
{
  Chocolaf::ChocolafApp::setupForHighDpiScreens();
  Chocolaf::ChocolafApp app(argc, argv);
  app.setStyle("Chocolaf");
  /*
  QApplication app(argc, argv);

  QFile f(":chocolaf/chocolaf.css");

  if (!f.exists()) {
     printf("Unable to open stylesheet!");
  } else {
     f.open(QFile::ReadOnly | QFile::Text);
     QTextStream ts(&f);
     app.setStyleSheet(ts.readAll());
  }
*/
  app.setApplicationName(app.translate("main", AppTitle.toStdString().c_str()));

  MainWindow mainWin;
  mainWin.show();

  return app.exec();
}
