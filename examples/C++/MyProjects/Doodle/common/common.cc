// common.cc - common functions
#include "common.hxx"
#include <QTextStream>
#include <QtCore>
#include <QtGui>
#include <QtWidgets>
#include <gmpxx.h> // GNU arbit precision numbers

QTextStream &operator<<(QTextStream &ost, const mpz_class &c)
{
   QString qstr(c.get_str().c_str());
   ost << qstr;
   return ost;
}

QColor getPaletteColor(QPalette::ColorRole colorRole, QPalette::ColorGroup colorGroup/*= QPalette::Active*/)
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
  }
  else if (QOperatingSystemVersion::current().majorVersion() > 10) {
    return true;
  }
  else {
    return false;
  }
}

bool windowsIsInDarkTheme()
{
  QSettings
    settings("HKEY_CURRENT_"
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

#endif
