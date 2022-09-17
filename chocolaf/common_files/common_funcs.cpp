#include "common_funcs.h"
#include <QTextStream>
#include <QtCore>

#ifndef _MSC_VER
#include <gmpxx.h> // GNU arbit precision numbers

QTextStream &operator << (QTextStream &ost, const std::string &str)
{
   // ost << QString::fromStdString(str);
   ost << QString::fromUtf8(str.data(), int(str.size()));
   return ost;
}

QTextStream &operator << (QTextStream &ost, const mpz_class &c)
{
   QString qstr(c.get_str().c_str());
   ost << qstr;
   return ost;
}

QDebug operator << (QDebug debug, const mpz_class &c)
{
   QDebugStateSaver saver(debug);
   QString qstr(c.get_str().c_str());
   debug.nospace() << qstr;
   return debug;
}
#endif

bool windowsDarkThemeAvailable()
{
#ifdef Q_OS_WINDOWS
   // dark mode supported Windows 10 1809 10.0.17763 onward
   // https://stackoverflow.com/questions/53501268/win10-dark-theme-how-to-use-in-winapi
   if (QOperatingSystemVersion::current().majorVersion() == 10) {
      return QOperatingSystemVersion::current().microVersion() >= 17763;
   } else if (QOperatingSystemVersion::current().majorVersion() > 10) {
      return true;
   } else {
      return false;
   }
#else
   return false;
#endif
}

bool windowsIsInDarkTheme()
{
#if defined Q_OS_WINDOWS
   QSettings settings(
         "HKEY_CURRENT_"
         "USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize",
         QSettings::NativeFormat);
   return settings.value("AppsUseLightTheme", 1).toInt() == 0;
#else
   return false;
#endif
}
