// ChocolafApp.cpp - ChocolafApp class implementation
#include "chocolaf.h"
#include <QApplication>
#include <QDebug>
#include <QFile>
#include <QMessageBox>
#include <QScreen>
#include <QStyleFactory>
#include <QTextStream>
#include <exception>
#ifdef Q_OS_WIN
#  include <windows.h>
#  include <winuser.h>
#  if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
#    include <shellscalingapi.h>   // for SetProcessDpiAwareness
#  endif
#endif   // Q_OS_WIN

namespace Chocolaf {

  // const struct __ChocolafPalette ChocolafPalette;
  const QString __version__ = {"1.0"};
  const QString __author__ = {"Manish Bhobé"};
  const QString __organization__ = {"Nämostuté Ltd."};
  const QString __domain__ = {"namostute.qtpyapps.in"};
  static QPalette *__palette = getPalette();

  QPalette *getPalette()
  {
    QPalette *palette = new QPalette();

    palette->setColor(QPalette::Window,
                      ChocolafPalette::Window_Color);   // general background color
    palette->setColor(QPalette::WindowText,
                      ChocolafPalette::WindowText_Color);   // general foreground color
    palette->setColor(QPalette::Base,
                      ChocolafPalette::Base_Color);   // background for text entry widgets
    // background color for views with alternating colors
    palette->setColor(QPalette::AlternateBase, ChocolafPalette::AlternateBase_Color);
    palette->setColor(QPalette::ToolTipBase,
                      ChocolafPalette::ToolTipBase_Color);   // background for tooltips
    palette->setColor(QPalette::ToolTipText, ChocolafPalette::ToolTipText_Color);
    palette->setColor(QPalette::Text,
                      ChocolafPalette::Text_Color);   // foreground color to use with Base
    palette->setColor(QPalette::Button,
                      ChocolafPalette::Button_Color);   // pushbutton colors
    palette->setColor(QPalette::ButtonText,
                      ChocolafPalette::ButtonText_Color);   // pushbutton's text color
    palette->setColor(QPalette::Link, ChocolafPalette::Link_Color);
    palette->setColor(QPalette::LinkVisited, ChocolafPalette::LinkVisited_Color);
    palette->setColor(QPalette::Highlight,
                      ChocolafPalette::Highlight_Color);   // highlight color
    palette->setColor(QPalette::HighlightedText, ChocolafPalette::HighlightedText_Color);
    // colors for disabled elements
    palette->setColor(QPalette::Disabled,
                      QPalette::ButtonText,
                      ChocolafPalette::Disabled_ButtonText_Color);
    palette->setColor(QPalette::Disabled,
                      QPalette::WindowText,
                      ChocolafPalette::Disabled_WindowText_Color);
    palette->setColor(QPalette::Disabled,
                      QPalette::Text,
                      ChocolafPalette::Disabled_Text_Color);
    palette->setColor(QPalette::Disabled,
                      QPalette::Light,
                      ChocolafPalette::Disabled_Light_Color);

    return palette;
  }

  void setStyleSheet(QApplication &app)
  {
    QFile f(":chocolaf/chocolaf.css");
    if (!f.exists()) {
      printf("Unable to open Chocolaf stylesheet! Falling back on Fusion style.");
      app.setStyle("Fusion");
    }
    else {
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

  void centerOnScreenWithSize(QWidget &widget, float widthProp, float heightProp)
  {
    // center the widget on screen
    QRect screenGeom = QGuiApplication::primaryScreen()->geometry();
    int widgetWidth = int(widthProp * screenGeom.width());
    int widgetHeight = int(heightProp * screenGeom.height());
    widget.resize(QSize(widgetWidth, widgetHeight));

    int x = int((screenGeom.width() - widget.width()) / 2);
    int y = int((screenGeom.height() - widget.height()) / 2);
    widget.move(x, y);
  }

  ChocolafApp::ChocolafApp(int argc, char *argv[]) : QApplication(argc, argv)
  {
    Q_ASSERT(__palette != nullptr);
    _palette = __palette;
    _styleSheet = QString("");
    // Nämostuté - sanskrit word tranlating to "May our minds meet"
    QApplication::setOrganizationName(__organization__);
    QApplication::setOrganizationDomain(__domain__);
    setPalette(*__palette);
    //_styleSheet = loadStyleSheet();
    for (auto a = 0; a < argc; ++a)
      qDebug() << "arg[" << a << "] = " << argv[a];
  }

  ChocolafApp::~ChocolafApp()
  {
    /* delete _palette;  */
  }

  void ChocolafApp::setStyle(const QString &styleName)
  {
    if (styleName == QString("Chocolaf")) {
      setFont(QApplication::font("QMenu"));

      QFile f(":chocolaf/chocolaf.css");
      if (!f.exists()) {
        printf("Unable to open Chocolaf stylesheet! Falling back on Fusion style.");
        QApplication::setStyle("Fusion");
      }
      else {
        f.open(QFile::ReadOnly | QFile::Text);
        QTextStream ts(&f);
        setStyleSheet(ts.readAll());
        // also set color palette
        Q_ASSERT(_palette != nullptr);
        setPalette(*_palette);
        // set other attributes as well
        setOrganizationName("Nämostuté Ltd.");
        setOrganizationDomain("namostute.qtpyapps.in");
      }
    }
    else if (QStyleFactory::keys().count(styleName) > 0) {
      QApplication::setStyle(styleName);
    }
    else {
      QString err = QString("Error: unrecognized style \'%1\'").arg(styleName);
      QMessageBox::critical(nullptr, "FATAL ERROR", err);
      throw std::invalid_argument(err.toStdString().c_str());
    }
  }

  // static
  void ChocolafApp::setupForHighDpiScreens()
  {
#ifdef Q_OS_WIN

#  if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
     ::SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE);
#  else
     ::SetProcessDPIAware();   // call before the main event loop
#  endif

#  if QT_VERSION >= QT_VERSION_CHECK(5, 6, 0)
     QApplication::setAttribute(Qt::AA_DisableHighDpiScaling);
     QApplication::setAttribute(Qt::AA_UseHighDpiPixmaps);
#  endif

#else
     // non Windows
#  if QT_VERSION >= QT_VERSION_CHECK(5, 6, 0)
     QApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
     QApplication::setAttribute(Qt::AA_UseHighDpiPixmaps);
#  endif

#endif
   }

   // static
   int ChocolafApp::pixelsToPoints(int pixels)
   {
      // NOTE: 1 inch == 96 pixels and 1 inch == 72 points
      // hence 96 pixels = 72 points
      return static_cast<int>(pixels * 72 / 96);
   }

   // static
   int ChocolafApp::pointsToPixels(int points)
   {
      // NOTE: 1 inch == 96 pixels and 1 inch == 72 points
      // hence 96 pixels = 72 points
      return static_cast<int>(points * 96 / 72);
   }

   /*-------------------------------------------------
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

}   // namespace Chocolaf
