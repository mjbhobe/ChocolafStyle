#include "common_funcs.h"
#include <QTextStream>
#include <QtCore>
#include <QtGui>
#include <QtWidgets>

#ifndef _MSC_VER
#include <gmpxx.h> // GNU arbit precision numbers

QTextStream &operator<<(QTextStream &ost, const mpz_class &c) 
{
   QString qstr(c.get_str().c_str());
   ost << qstr;
   return ost;
}
#endif

QColor getPaletteColor(QPalette::ColorRole colorRole, QPalette::ColorGroup colorGroup /*= QPalette::Active*/)
{
   QPalette pal = qApp->palette();
   QColor color = pal.color(colorGroup, colorRole);
   return color;
}

#ifdef Q_OS_WINDOWS

bool windowsDarkThemeAvailable()
{
   // dark mode supported Windows 10 1809 10.0.17763 onward
   // https://stackoverflow.com/questions/53501268/win10-dark-theme-how-to-use-in-winapi
   if (QOperatingSystemVersion::current().majorVersion() == 10) {
      return QOperatingSystemVersion::current().microVersion() >= 17763;
   } else if (QOperatingSystemVersion::current().majorVersion() > 10) {
      return true;
   } else {
      return false;
   }
}

bool windowsIsInDarkTheme()
{
   QSettings settings("HKEY_CURRENT_"
                      "USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize",
                      QSettings::NativeFormat);
   return settings.value("AppsUseLightTheme", 1).toInt() == 0;
}

void setWinDarkPalette(QApplication *app)
{
   // @see: https://github.com/Jorgen-VikingGod/Qt-Frameless-Window-DarkStyle/blob/master/DarkStyle.cpp
   QPalette palette;

   palette.setColor(QPalette::Window, QColor(53, 53, 53));
   palette.setColor(QPalette::WindowText, Qt::white);
   palette.setColor(QPalette::Disabled, QPalette::WindowText, QColor(127, 127, 127));
   palette.setColor(QPalette::Base, QColor(42, 42, 42));
   palette.setColor(QPalette::AlternateBase, QColor(66, 66, 66));
   palette.setColor(QPalette::ToolTipBase, Qt::white);
   palette.setColor(QPalette::ToolTipText, QColor(53, 53, 53));
   palette.setColor(QPalette::Text, Qt::white);
   palette.setColor(QPalette::Disabled, QPalette::Text, QColor(127, 127, 127));
   palette.setColor(QPalette::Dark, QColor(35, 35, 35));
   palette.setColor(QPalette::Shadow, QColor(20, 20, 20));
   palette.setColor(QPalette::Button, QColor(53, 53, 53));
   palette.setColor(QPalette::ButtonText, Qt::white);
   palette.setColor(QPalette::Disabled, QPalette::ButtonText, QColor(127, 127, 127));
   palette.setColor(QPalette::BrightText, Qt::red);
   palette.setColor(QPalette::Link, QColor(42, 130, 218));
   palette.setColor(QPalette::Highlight, QColor(42, 130, 218));
   palette.setColor(QPalette::Disabled, QPalette::Highlight, QColor(80, 80, 80));
   palette.setColor(QPalette::HighlightedText, Qt::white);
   palette.setColor(QPalette::Disabled, QPalette::HighlightedText, QColor(127, 127, 127));

   /*
   palette.setColor(QPalette::Window, QColor(53, 53, 53));
   palette.setColor(QPalette::WindowText, Qt::white);
   palette.setColor(QPalette::Disabled, QPalette::WindowText, QColor(127, 127, 127));
   palette.setColor(QPalette::PlaceholderText, QColor(130, 130, 130));
   palette.setColor(QPalette::Base, QColor(25, 25, 25));           // QColor(30, 30, 30));
   palette.setColor(QPalette::AlternateBase, QColor(53, 53, 53));  // QColor(35, 35, 35));
   palette.setColor(QPalette::ToolTipBase, QColor(255, 255, 225)); // Qt::black);
   palette.setColor(QPalette::ToolTipText, QColor(53, 53, 53));
   palette.setColor(QPalette::Text, Qt::white);
   palette.setColor(QPalette::Disabled, QPalette::Text, QColor(127, 127, 127));
   palette.setColor(QPalette::Button, QColor(53, 53, 53));
   palette.setColor(QPalette::ButtonText, Qt::white);
   palette.setColor(QPalette::Disabled, QPalette::ButtonText, QColor(127, 127, 127));
   palette.setColor(QPalette::BrightText, Qt::red);
   palette.setColor(QPalette::Link, QColor(42, 130, 218));
   palette.setColor(QPalette::Highlight, QColor(0, 120, 215)); // QColor(42, 130, 218));
   palette.setColor(QPalette::Disabled, QPalette::Highlight, QColor(80, 80, 80));
   palette.setColor(QPalette::HighlightedText, Qt::white);
   palette.setColor(QPalette::Disabled, QPalette::HighlightedText, QColor(127, 127, 127));
   palette.setColor(QPalette::Dark, QColor(35, 35, 35));
   palette.setColor(QPalette::Shadow, QColor(20, 20, 20));
   palette.setColor(QPalette::Shadow, QColor(55, 55, 55));
   */

   qDebug("Before setting palette: %s",
          qPrintable(palette.color(QPalette::Active, QPalette::ColorRole(QPalette::Window)).name()));
   app->setPalette(palette);
   QPalette p = qApp->palette();
   qDebug("After setting palette: %s",
          qPrintable(p.color(QPalette::Active, QPalette::ColorRole(QPalette::Window)).name()));
   // QGuiApplication::setPalette(palette);
}

PaletteSwitcher::PaletteSwitcher(QApplication *appInstance, QObject *parent /*=nullptr*/)
   : QObject(parent), _appInstance{appInstance}, _darkPalette{new QPalette()}, _lightPalette{new QPalette()},
     darkPaletteInUse{false}
{
   Q_ASSERT(appInstance != nullptr);
   initializePalettes();
   darkPaletteInUse = (windowsDarkThemeAvailable() && windowsIsInDarkTheme());
   if (darkPaletteInUse)
      _appInstance->setPalette(*_darkPalette);
   else
      _appInstance->setPalette(*_lightPalette);
}

PaletteSwitcher::~PaletteSwitcher()
{
   delete _lightPalette;
   delete _darkPalette;
}

void PaletteSwitcher::swapPalettes()
{
   if (darkPaletteInUse)
      _appInstance->setPalette(*_lightPalette);
   else
      _appInstance->setPalette(*_darkPalette);
   darkPaletteInUse = !darkPaletteInUse;
}

void PaletteSwitcher::initializePalettes()
{
   Q_ASSERT(_darkPalette != nullptr);
   // general backround color
   _darkPalette->setColor(QPalette::Window, QColor(38, 38, 38) /* QColor(53, 53, 53) */);
   _darkPalette->setColor(QPalette::WindowText, Qt::white);
   _darkPalette->setColor(QPalette::Disabled, QPalette::WindowText, QColor(127, 127, 127));
   // background color for most widgets
   _darkPalette->setColor(QPalette::Base, QColor(54, 54, 54) /* QColor(42, 42, 42) */);
   // background color for alternate views
   _darkPalette->setColor(QPalette::AlternateBase, QColor(66, 66, 66));
   _darkPalette->setColor(QPalette::ToolTipBase, Qt::white);
   _darkPalette->setColor(QPalette::ToolTipText, QColor(53, 53, 53));
   _darkPalette->setColor(QPalette::Text, Qt::white);
   _darkPalette->setColor(QPalette::Disabled, QPalette::Text, QColor(127, 127, 127));
   _darkPalette->setColor(QPalette::Dark, QColor(35, 35, 35));
   _darkPalette->setColor(QPalette::Shadow, QColor(20, 20, 20));
   _darkPalette->setColor(QPalette::Button, QColor(53, 53, 53));
   _darkPalette->setColor(QPalette::ButtonText, Qt::white);
   _darkPalette->setColor(QPalette::Disabled, QPalette::ButtonText, QColor(127, 127, 127));
   _darkPalette->setColor(QPalette::BrightText, Qt::red);
   _darkPalette->setColor(QPalette::Link, QColor(42, 130, 218));
   _darkPalette->setColor(QPalette::Highlight, QColor(42, 130, 218));
   _darkPalette->setColor(QPalette::Disabled, QPalette::Highlight, QColor(80, 80, 80));
   _darkPalette->setColor(QPalette::HighlightedText, Qt::white);
   _darkPalette->setColor(QPalette::Disabled, QPalette::HighlightedText, QColor(127, 127, 127));

   Q_ASSERT(_lightPalette != nullptr);
   _lightPalette->setColor(QPalette::Window, QColor(240, 240, 240));
   _lightPalette->setColor(QPalette::WindowText, Qt::black);
   _lightPalette->setColor(QPalette::Disabled, QPalette::WindowText, QColor(240, 240, 240));
   _lightPalette->setColor(QPalette::Base, Qt::white);
   _lightPalette->setColor(QPalette::AlternateBase, QColor(233, 231, 227));
   _lightPalette->setColor(QPalette::ToolTipBase, QColor(255, 255, 220));
   _lightPalette->setColor(QPalette::ToolTipText, Qt::black);
   _lightPalette->setColor(QPalette::Text, Qt::black);
   _lightPalette->setColor(QPalette::Disabled, QPalette::Text, QColor(120, 120, 120));
   _lightPalette->setColor(QPalette::Dark, QColor(160, 160, 160));
   _lightPalette->setColor(QPalette::Shadow, QColor(105, 105, 105));
   _lightPalette->setColor(QPalette::Button, QColor(240, 240, 240));
   _lightPalette->setColor(QPalette::ButtonText, Qt::black);
   _lightPalette->setColor(QPalette::Disabled, QPalette::ButtonText, QColor(78, 78, 78));
   _lightPalette->setColor(QPalette::BrightText, Qt::white);
   _lightPalette->setColor(QPalette::Link, QColor(0, 0, 255));
   _lightPalette->setColor(QPalette::Highlight, QColor(0, 120, 215));
   _lightPalette->setColor(QPalette::Disabled, QPalette::Highlight, QColor(0, 120, 215));
   _lightPalette->setColor(QPalette::HighlightedText, Qt::white);
   _lightPalette->setColor(QPalette::Disabled, QPalette::HighlightedText, Qt::white);
}

#endif
