// Copyright (C) 2016 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

#include <QApplication>

#include "chocolaf.h"
#include "tabdialog.h"

int main(int argc, char *argv[])
{
  // QApplication app(argc, argv);
  Chocolaf::ChocolafApp::setupForHighDpiScreens();
  Chocolaf::ChocolafApp app(argc, argv);
  app.setStyle("Fusion");

  QString fileName;

  if (argc >= 2)
    fileName = argv[1];
  else
    fileName = ".";

  TabDialog tabdialog(fileName);
  tabdialog.show();

  return app.exec();
}
