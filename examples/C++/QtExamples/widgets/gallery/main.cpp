// Copyright (C) 2020 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

#include "chocolaf.h"
#include "widgetgallery.h"
#include <QApplication>
#include <QPalette>
#include <QSettings>
#include <QStyleFactory>

void setDarkPalette(QApplication *app)
{
#ifdef Q_OS_WIN
   QSettings
      settings("HKEY_CURRENT_"
               "USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize",
               QSettings::NativeFormat);
   app->setStyle(QStyleFactory::create("Fusion"));
   if (settings.value("AppsUseLightTheme") == 0) {
      QPalette darkPalette;
      QColor darkColor = QColor(45, 45, 45);
      QColor disabledColor = QColor(127, 127, 127);
      darkPalette.setColor(QPalette::Window, darkColor);
      darkPalette.setColor(QPalette::WindowText, Qt::white);
      darkPalette.setColor(QPalette::Base, QColor(18, 18, 18));
      darkPalette.setColor(QPalette::AlternateBase, darkColor);
      darkPalette.setColor(QPalette::ToolTipBase, Qt::white);
      darkPalette.setColor(QPalette::ToolTipText, Qt::white);
      darkPalette.setColor(QPalette::Text, Qt::white);
      darkPalette.setColor(QPalette::Disabled, QPalette::Text, disabledColor);
      darkPalette.setColor(QPalette::Button, darkColor);
      darkPalette.setColor(QPalette::ButtonText, Qt::white);
      darkPalette.setColor(QPalette::Disabled, QPalette::ButtonText, disabledColor);
      darkPalette.setColor(QPalette::BrightText, Qt::red);
      darkPalette.setColor(QPalette::Link, QColor(42, 130, 218));

      darkPalette.setColor(QPalette::Highlight, QColor(42, 130, 218));
      darkPalette.setColor(QPalette::HighlightedText, Qt::black);
      darkPalette.setColor(QPalette::Disabled, QPalette::HighlightedText, disabledColor);

      app->setPalette(darkPalette);

      qApp->setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: "
                          "1px solid white; }");
   }
#endif
}

int main(int argc, char *argv[])
{
   //   QApplication app(argc, argv);
   //   setDarkPalette(&app);

   Chocolaf::ChocolafApp::setupForHighDpiScreens();
   Chocolaf::ChocolafApp app(argc, argv);
   //#ifdef Q_OS_WIN
   //   app.setStyle("WindowsDark");
   //#else
   //   app.setStyle("Chocolaf");
   //#endif
   app.setStyle("Chocolaf");

   WidgetGallery gallery;
   gallery.show();

   // return QCoreApplication::exec();
   return app.exec();
}
