// ChocolafApp.cpp - ChocolafApp class implementation
#include "chocolaf.h"
#include <QApplication>
#include <QDebug>
#include <QFile>
#include <QMessageBox>
#include <QStyleFactory>
#include <QTextStream>
#include <exception>

namespace Chocolaf {

   // const struct __ChocolafPalette ChocolafPalette;
   const QString __version__ = {"1.0"};
   const QString __author__ = {"Manish Bhobé"};
   static QPalette *__palette = getPalette();

   QPalette *getPalette()
   {
      QPalette *palette = new QPalette();

      palette->setColor(QPalette::Window,
                        ChocolafPalette::Window_Color); // general background color
      palette->setColor(QPalette::WindowText,
                        ChocolafPalette::WindowText_Color); // general foreground color
      palette->setColor(QPalette::Base,
                        ChocolafPalette::Base_Color); // background for text entry widgets
      // background color for views with alternating colors
      palette->setColor(QPalette::AlternateBase, ChocolafPalette::AlternateBase_Color);
      palette->setColor(QPalette::ToolTipBase,
                        ChocolafPalette::ToolTipBase_Color); // background for tooltips
      palette->setColor(QPalette::ToolTipText, ChocolafPalette::ToolTipText_Color);
      palette->setColor(QPalette::Text,
                        ChocolafPalette::Text_Color); // foreground color to use with Base
      palette->setColor(QPalette::Button,
                        ChocolafPalette::Button_Color); // pushbutton colors
      palette->setColor(QPalette::ButtonText,
                        ChocolafPalette::ButtonText_Color); // pushbutton's text color
      palette->setColor(QPalette::Link, ChocolafPalette::Link_Color);
      palette->setColor(QPalette::LinkVisited, ChocolafPalette::LinkVisited_Color);
      palette->setColor(QPalette::Highlight,
                        ChocolafPalette::Highlight_Color); // highlight color
      palette->setColor(QPalette::HighlightedText,
                        ChocolafPalette::HighlightedText_Color);
      // colors for disabled elements
      palette->setColor(QPalette::Disabled, QPalette::ButtonText,
                        ChocolafPalette::Disabled_ButtonText_Color);
      palette->setColor(QPalette::Disabled, QPalette::WindowText,
                        ChocolafPalette::Disabled_WindowText_Color);
      palette->setColor(QPalette::Disabled, QPalette::Text,
                        ChocolafPalette::Disabled_Text_Color);
      palette->setColor(QPalette::Disabled, QPalette::Light,
                        ChocolafPalette::Disabled_Light_Color);

      return palette;
   }

   void setStyleSheet(QApplication &app)
   {
      QFile f(":chocolaf/chocolaf.css");
      if (!f.exists()) {
         printf("Unable to open Chocolaf stylesheet! Falling back on Fusion style.");
         app.setStyle("Fusion");
      } else {
         f.open(QFile::ReadOnly | QFile::Text);
         QTextStream ts(&f);
         app.setStyleSheet(ts.readAll());
         // also set color palette
         Q_ASSERT(__palette != nullptr);
         app.setPalette(*__palette);
         // set other attributes as well
         app.setOrganizationName("Nämostuté Ltd.");
         app.setOrganizationDomain("namostute.qtpyapps.in");
      }
   }

   /* ---------------------------
      ChocolafApp::ChocolafApp(int argc, char *argv[]) : QApplication(argc, argv)
      {
         _palette = getPalette();
         _styleSheet = QString("");
         // Nämostuté - sanskrit word tranlating to "May our minds meet"
         QApplication::setOrganizationName("Nämostuté Ltd.");
         QApplication::setOrganizationDomain("namostute.qtpyapps.in");
         / *
         _palette = getPalette();
         Q_ASSERT(_palette != nullptr);
         _styleSheet = loadStyleSheet();
         * /
         for (auto a = 0; a < argc; ++a)
            qDebug() << "arg[" << a << "] = " << argv[a];
      }

      ChocolafApp::~ChocolafApp() { delete _palette; }

      void ChocolafApp::setStyle(const QString &styleName)
      {
         if (styleName == QString("Chocolaf")) {
            setFont(QApplication::font("QMenu"));
            QApplication::setPalette(*_palette);

            QFile f(":chocolaf/chocolaf.css");
            if (!f.exists()) {
               QMessageBox::critical(nullptr, QString("FATAL ERROR"),
                                     QString("Unable to load chocolaf stylesheet from "
                                             ":chocolaf/chocolaf.css\r\n"
                                             "Falling back to Fusion style."));
               QApplication::setStyle("Fusion");
            } else {
               f.open(QFile::ReadOnly | QFile::Text);
               QTextStream ts(&f);
               QApplication::setStyleSheet(ts.readAll());
            }
         } else if (QStyleFactory::keys().count(styleName) > 0) {
            QApplication::setStyle(styleName);
         } else {
            QString err = QString("Error: unrecognized style \'%1\'").arg(styleName);
            QMessageBox::critical(nullptr, "FATAL ERROR", err);
            throw std::invalid_argument(err.toStdString().c_str());
         }
      }

      QString ChocolafApp::loadStyleSheet()
      {
         QFile f(":chocolaf/chocolaf.css");

         if (!f.exists()) {
            QMessageBox::critical(nullptr, QString("FATAL ERROR"),
                                  QString("Unable to load chocolaf stylesheet from "
                                          ":chocolaf/chocolaf.css"));
            return "";
         } else {
            f.open(QFile::ReadOnly | QFile::Text);
            QTextStream ts(&f);
            return ts.readAll();
         }
      }

      QPalette *ChocolafApp::getPalette()
      {
         QPalette *palette = new QPalette();

         palette->setColor(QPalette::Window,
                           ChocolafPalette::Window_Color); // general background color
         palette->setColor(QPalette::WindowText,
                           ChocolafPalette::WindowText_Color); // general foreground color
         palette->setColor(QPalette::Base,
                           ChocolafPalette::Base_Color); // background for text entry
      widgets
         // background color for views with alternating colors
         palette->setColor(QPalette::AlternateBase, ChocolafPalette::AlternateBase_Color);
         palette->setColor(QPalette::ToolTipBase,
                           ChocolafPalette::ToolTipBase_Color); // background for tooltips
         palette->setColor(QPalette::ToolTipText, ChocolafPalette::ToolTipText_Color);
         palette->setColor(QPalette::Text,
                           ChocolafPalette::Text_Color); // foreground color to use with
      Base palette->setColor(QPalette::Button, ChocolafPalette::Button_Color); //
      pushbutton colors palette->setColor(QPalette::ButtonText,
                           ChocolafPalette::ButtonText_Color); // pushbutton's text color
         palette->setColor(QPalette::Link, ChocolafPalette::Link_Color);
         palette->setColor(QPalette::LinkVisited, ChocolafPalette::LinkVisited_Color);
         palette->setColor(QPalette::Highlight,
                           ChocolafPalette::Highlight_Color); // highlight color
         palette->setColor(QPalette::HighlightedText,
                           ChocolafPalette::HighlightedText_Color);
         // colors for disabled elements
         palette->setColor(QPalette::Disabled, QPalette::ButtonText,
                           ChocolafPalette::Disabled_ButtonText_Color);
         palette->setColor(QPalette::Disabled, QPalette::WindowText,
                           ChocolafPalette::Disabled_WindowText_Color);
         palette->setColor(QPalette::Disabled, QPalette::Text,
                           ChocolafPalette::Disabled_Text_Color);
         palette->setColor(QPalette::Disabled, QPalette::Light,
                           ChocolafPalette::Disabled_Light_Color);

         return palette;
      }
       ----------------------------------- */

} // namespace Chocolaf
