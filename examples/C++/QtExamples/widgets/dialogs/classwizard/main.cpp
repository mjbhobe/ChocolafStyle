// Copyright (C) 2016 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

#include <QApplication>
#include <QLibraryInfo>
#include <QLocale>
#include <QTranslator>

#include "chocolaf.h"
#include "classwizard.h"

int main(int argc, char *argv[])
{
   Q_INIT_RESOURCE(classwizard);

   // QApplication app(argc, argv);
   Chocolaf::ChocolafApp::setupForHighDpiScreens();
   Chocolaf::ChocolafApp app(argc, argv);

   //#ifdef Q_OS_WIN
   //   app.setStyle("WindowsDark");
   //#else
   //   app.setStyle("Chocolaf");
   //#endif
   app.setStyle("Chocolaf");

#ifndef QT_NO_TRANSLATION
   QString translatorFileName = QLatin1String("qtbase_");
   translatorFileName += QLocale::system().name();
   QTranslator *translator = new QTranslator(&app);
   if (translator->load(translatorFileName,
                        QLibraryInfo::path(QLibraryInfo::TranslationsPath)))
      app.installTranslator(translator);
#endif

   ClassWizard wizard;
   wizard.show();
   return app.exec();
}
