// ch02/findDialog/main.cc: main
#include "mainwin.h"
#include <QApplication>
#include <QDialog>

int main(int argc, char **argv)
{
  QApplication app(argc, argv);
  QApplication::setFont(QApplication::font("QMenu"));
  app.setStyle("Fusion");

  MainWin *mainWin = new MainWin();
  //GoToCellDialog *dlg = new GoToCellDialog();
  mainWin->setFont(QApplication::font("QMenu"));
  mainWin->show();

  return app.exec();
}
