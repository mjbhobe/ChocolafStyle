// Copyright (C) 2020 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

#include "chocolaf.h"
#include "widgetgallery.h"
#include <QApplication>
#include <QPalette>
#include <QSettings>
#include <QStyleFactory>

/*
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
      darkPalette.setColor(QPalette::Window,
                           WinDarkPalette::Window_Color); // general background color
      darkPalette.setColor(QPalette::WindowText,
                           WinDarkPalette::WindowText_Color); // general foreground color
      darkPalette.setColor(QPalette::Base,
                           WinDarkPalette::Base_Color); // background for text entry widgets
      // background color for views with alternating colors
      darkPalette.setColor(QPalette::AlternateBase, WinDarkPalette::AlternateBase_Color);
      darkPalette.setColor(QPalette::ToolTipBase,
                           WinDarkPalette::ToolTipBase_Color); // background for tooltips
      darkPalette.setColor(QPalette::ToolTipText, WinDarkPalette::ToolTipText_Color);
      darkPalette.setColor(QPalette::Text,
                           WinDarkPalette::Text_Color); // foreground color to use with Base
      darkPalette.setColor(QPalette::Button,
                           WinDarkPalette::Button_Color); // pushbutton colors
      darkPalette.setColor(QPalette::ButtonText,
                           WinDarkPalette::ButtonText_Color); // pushbutton's text color
      darkPalette.setColor(QPalette::Link, WinDarkPalette::Link_Color);
      darkPalette.setColor(QPalette::LinkVisited, WinDarkPalette::LinkVisited_Color);
      darkPalette.setColor(QPalette::Highlight,
                           WinDarkPalette::Highlight_Color); // highlight color
      darkPalette.setColor(QPalette::HighlightedText,
                           WinDarkPalette::HighlightedText_Color);
      // colors for disabled elements
      darkPalette.setColor(QPalette::Disabled, QPalette::ButtonText,
                           WinDarkPalette::Disabled_ButtonText_Color);
      darkPalette.setColor(QPalette::Disabled, QPalette::WindowText,
                           WinDarkPalette::Disabled_WindowText_Color);
      darkPalette.setColor(QPalette::Disabled, QPalette::Text,
                           WinDarkPalette::Disabled_Text_Color);
      darkPalette.setColor(QPalette::Disabled, QPalette::Light,
                           WinDarkPalette::Disabled_Light_Color);

      app->setPalette(darkPalette);

      qApp->setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: "
                          "1px solid white; }");
   }
#endif
}
*/

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
