// main.cc - launcher
#include <QtCore>
#include <QtGui>
#include <QtWidgets>
#include "FindDialog.h"
#include "common_funcs.h"

QTextStream cout(stdout, QIODevice::WriteOnly);
QTextStream cerr(stderr, QIODevice::WriteOnly);
QTextStream cin(stdin, QIODevice::ReadOnly);

int main(int argc, char **argv)
{
  QApplication app(argc, argv);
  app.setStyle("Fusion");
  QFont font("SF UI Text", QApplication::font("QMenu").pointSize());
  //PaletteSwitcher palSwitcher(&app);
  
  // using QDarkStyle
  QFile file(":qdarkstyle/dark/style.qss");

  if (!file.exists()) {
    cerr << "Unable to set dark stylesheet! File not found" << Qt::endl;
  }
  else {
    file.open(QFile::ReadOnly | QFile::Text);
    QTextStream ts(&file);
    app.setStyleSheet(ts.readAll());
  }

  //if (windowsDarkThemeAvailable() && windowsIsInDarkTheme())
  //  palSwitcher.setDarkPalette();

  FindDialog findDlg;
  findDlg.setFont(font);
  findDlg.show();

  return app.exec();
}
