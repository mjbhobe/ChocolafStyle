#include "common_funcs.h"
#include <QFileInfo>
#include <QTextStream>
#include <QtCore>

#ifndef _MSC_VER
#include <gmpxx.h> // GNU arbit precision numbers

QTextStream &operator<<(QTextStream &ost, const std::string &str)
{
  // ost << QString::fromStdString(str);
  ost << QString::fromUtf8(str.data(), int(str.size()));
  return ost;
}

QTextStream &operator<<(QTextStream &ost, const mpz_class &c)
{
  QString qstr(c.get_str().c_str());
  ost << qstr;
  return ost;
}

QDebug operator<<(QDebug debug, const mpz_class &c)
{
  QString qstr(c.get_str().c_str());
  debug.nospace() << qstr;
  return debug;
}
#endif

// helper functions to read from console
bool getline(QTextStream &in, std::string &ret, const QString &prompt /*=""*/)
{
#ifdef USING_QT6
  QTextStream out(stdout, QIODeviceBase::WriteOnly);
#else
  QTextStream out(stdout, QIODevice::WriteOnly);
#endif

  if (prompt != "") {
    out << prompt << Qt::flush;
  }
  QString str = in.readLine();
  if (in.atEnd())
    return false;
  ret = str.toStdString();
  return true;
}

bool getline(QTextStream &in, QString &ret, const QString &prompt /*=""*/)
{
#ifdef USING_QT6
  QTextStream out(stdout, QIODeviceBase::WriteOnly);
#else
  QTextStream out(stdout, QIODevice::WriteOnly);
#endif

  if (prompt != "") {
    out << prompt << Qt::flush;
  }
  QString str = in.readLine();
  if (in.atEnd())
    return false;
  ret = str;
  return true;
}

bool readString(QTextStream &in, QString &ret, const QString &prompt /*= ""*/)
{
  return getline(in, ret, prompt);
}

bool readInt(QTextStream &in, int &ret, const QString &prompt /*= ""*/)
{
#ifdef USING_QT6
  QTextStream out(stdout, QIODeviceBase::WriteOnly);
#else
  QTextStream out(stdout, QIODevice::WriteOnly);
#endif
  bool ok = false;

  if (prompt != "") {
    out << prompt << Qt::flush;
  }
  QString line = in.readLine();
  ret = line.toInt(&ok);
  return ok;
}

bool readDouble(QTextStream &in, double &ret, const QString &prompt /*= ""*/)
{
#ifdef USING_QT6
  QTextStream out(stdout, QIODeviceBase::WriteOnly);
#else
  QTextStream out(stdout, QIODevice::WriteOnly);
#endif
  bool ok = false;

  if (prompt != "") {
    out << prompt << Qt::flush;
  }
  QString line = in.readLine();
  ret = line.toDouble(&ok);
  return ok;
}

bool fileExists(const QString &filepath)
{
  QFileInfo fileInfo(filepath);
  return fileInfo.exists();
}

bool windowsDarkThemeAvailable()
{
#ifdef Q_OS_WINDOWS
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
#else
  return false;
#endif
}

bool windowsIsInDarkTheme()
{
#if defined Q_OS_WINDOWS
  QSettings settings("HKEY_CURRENT_" "USER\\Software\\Microsoft\\Windows\\CurrentVersion"
                     "\\Themes\\Personalize",
                     QSettings::NativeFormat);
  return settings.value("AppsUseLightTheme", 1).toInt() == 0;
#else
  return false;
#endif
}
