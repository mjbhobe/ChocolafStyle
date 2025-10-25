#ifndef __common_funcs_h__
#define __common_funcs_h__

// #pragma GCC diagnostic ignored "-Wc++17-attribute-extensions"

#include <QTextStream>
#include <QtCore>
#include <chrono>
#include <ctime>
#include <format>
#include <locale>
#include <sstream>
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

// class to help you format numbers, currency & dates
// per your locale formatting rules
class LocaleFormatter {
private:
  std::locale _locale;

public:
  LocaleFormatter(std::locale locale)
    : _locale{locale}
  {
  }

  std::string formatAsNumber(double val)
  {
    std::stringstream ss;
    ss.imbue(_locale);

    ss << std::showbase << std::fixed << val;
    return ss.str();
  }

  std::string formatAsCurrency(double val)
  {
    std::stringstream ss;
    ss.imbue(_locale);

    // put_money for currency requires * 100
    ss << std::showbase << std::put_money(val * 100);
    return ss.str();
  }

  std::tm to_tm(const std::chrono::year_month_day &ymd)
  {
    std::tm tm_result{};
    tm_result.tm_year = static_cast<int>(ymd.year()) - 1900; // tm_year = years since 1900
    tm_result.tm_mon = static_cast<unsigned>(ymd.month()) - 1; // tm_mon = [0, 11]
    tm_result.tm_mday = static_cast<unsigned>(ymd.day());

    // Other fields you might want to default to 0
    tm_result.tm_hour = 0;
    tm_result.tm_min = 0;
    tm_result.tm_sec = 0;
    tm_result.tm_isdst = -1; // Not known whether DST is in effect

    return tm_result;
  }

  std::string formatAsDate(const std::chrono::year_month_day &date)
  {
    std::stringstream ss;
    ss.imbue(_locale);

    /* does not work with C++20 or C++23 - may work with C++26!
    std::chrono::sys_days day_point{date};
    ss << std::format(_locale, "{:L%x}", day_point); */

    std::tm tm = to_tm(date);
    ss << std::put_time(&tm, "%x");
    return ss.str();
  }
};

#endif // __common_funcs_h__
