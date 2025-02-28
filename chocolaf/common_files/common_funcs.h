#ifndef __common_funcs_h__
#define __common_funcs_h__

// #pragma GCC diagnostic ignored "-Wc++17-attribute-extensions"

#include <QTextStream>
#include <QtCore>
#include <string>

#if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
#define USING_QT6
#else
#define USING_QT5
#endif

#ifndef _MSC_VER
#include <gmpxx.h> // GNU arbit precision numbers
QTextStream &operator<<(QTextStream &ost, const std::string &str);
QTextStream &operator<<(QTextStream &ost, const mpz_class &c);
QDebug operator<<(QDebug debug, const mpz_class &c);
#endif

bool getline(QTextStream &in, std::string &ret, const QString &prompt = "");
bool getline(QTextStream &in, QString &ret, const QString &prompt = "");
bool readString(QTextStream &in, QString &ret, const QString &prompt = "");
bool readInt(QTextStream &in, int &ret, const QString &prompt = "");
bool readDouble(QTextStream &in, double &ret, const QString &prompt = "");
bool fileExists(const QString &filepath);

bool windowsDarkThemeAvailable();
bool windowsIsInDarkTheme();

#endif // __common_funcs_h__
