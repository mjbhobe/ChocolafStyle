// main.cpp - addressbook
#include "chocolaf.h"
#include "listDialog.h"
#include <QApplication>

int main(int argc, char **argv)
{
  //QApplication app(argc, argv);
  Chocolaf::ChocolafApp::setupForHighDpiScreens();
  Chocolaf::ChocolafApp app(argc, argv);
  app.setStyle("Chocolaf");

  ListDialog dlg;
  dlg.setWindowTitle(QString("Qt %1: Address Book").arg(QT_VERSION_STR));
  dlg.show();

  return app.exec();
}

