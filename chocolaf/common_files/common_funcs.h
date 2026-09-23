#ifndef __common_funcs_h__
#define __common_funcs_h__

// ---- Require a C++20 (or later) compliant compiler (clang++/g++/MSVC) ----
#if defined(_MSC_VER)
#if !defined(_MSVC_LANG) || _MSVC_LANG < 202002L
#error "Requires a C++20 (or later) compliant compiler. Compile with /std:c++20 (or newer) and /Zc:__cplusplus."
#endif
#else
#if __cplusplus < 202002L
#error "Requires a C++20 (or later) compliant compiler. Compile with -std=c++20 (or newer)."
#endif
#endif

// ---- Optional: detect a C++23 (or later) compiler ----
// std::chrono::year_month_day itself is a C++20 type, but standard-library
// support for std::chrono::parse()/calendar stream parsing has historically
// varied a lot across compilers (GCC/Clang/MSVC) even where the type is
// available - gate the year_month_day branch of DateTimeType behind an
// actual C++23 compiler as a conservative, cross-toolchain-safe check,
// rather than trusting that C++20 mode alone means parsing works.
#if defined(_MSC_VER)
#define CHOCOLAF_HAVE_CHRONO_PARSE (_MSVC_LANG >= 202302L)
#else
#define CHOCOLAF_HAVE_CHRONO_PARSE (__cplusplus >= 202302L)
#endif

// #pragma GCC diagnostic ignored "-Wc++17-attribute-extensions"

// ---- Build-flavour detection (single place to maintain) ----
#if defined(QT_WIDGETS_LIB) || defined(QT_QUICK_LIB) || defined(QT_QML_LIB) || defined(QT_GUI_LIB)
#define QT_GUI_BUILD 1
#else
#define QT_CONSOLE_BUILD 1
#endif

#include <QtGlobal>

#if QT_VERSION >= QT_VERSION_CHECK(6, 0, 0)
#define USING_QT6
#else
#define USING_QT5
#endif

#include <QTextStream>
#include <QString>
#include <QDebug>
#include <QDate>
#include <QTime>
#include <QDateTime>
#include <QLocale>
#include <chrono>
#include <concepts>
#include <ctime>
#include <iomanip>
#include <locale>
#include <sstream>
#include <stdexcept>
#include <string>

//@formatter:off

// concept definitions --------------------------------------------------------------------
// the character types: char, wchar_t, char8_t, char16_t, char32_t
template <typename T> concept CharType = std::same_as<T, char> || std::same_as<T, wchar_t> ||
  std::same_as<T, char8_t> || std::same_as<T, char16_t> || std::same_as<T, char32_t>;

// QString or std::string
template <typename T> concept StringType = std::same_as<T, QString> || std::same_as<T,
  std::string>;

// any integer type EXCLUDING bool, the character types, and the two
// single-byte integer types (signed char/unsigned char, i.e. qint8/quint8).
// The latter satisfy std::integral and aren't caught by CharType (which
// only lists the true "character" types), but readIntegerType()/
// parseIntegerType() have no dispatch branch for them either - without
// this exclusion, IntegerType<signed char> would be true yet every branch
// in those functions' if constexpr chains would silently fail to match,
// so ok would stay false for every input. Excluding them here turns that
// into a compile-time error at the call site instead of a silent
// always-fails bug at runtime.
template <typename T>
concept IntegerType = std::integral<T> && !std::same_as<T, bool> && !CharType<T> &&
                       !std::same_as<T, signed char> && !std::same_as<T, unsigned char>;

// float & double only - unlike integers, IEEE-754 floating-point types are
// always signed, so there is no "unsigned" variant to include here.
template <typename T> concept FloatType = std::same_as<T, float> || std::same_as<T, double>;

// QDate, QTime, QDateTime, the STL equivalent std::tm, and - only when
// compiled with a C++23 (or later) compiler, see CHOCOLAF_HAVE_CHRONO_PARSE
// above - the STL calendar type std::chrono::year_month_day
#if CHOCOLAF_HAVE_CHRONO_PARSE
template <typename T>
concept DateTimeType = std::same_as<T, QDate> || std::same_as<T, QTime> ||
                        std::same_as<T, QDateTime> || std::same_as<T, std::tm> ||
                        std::same_as<T, std::chrono::year_month_day>;
#else
template <typename T>
concept DateTimeType = std::same_as<T, QDate> || std::same_as<T, QTime> ||
                        std::same_as<T, QDateTime> || std::same_as<T, std::tm>;
#endif
// concept definitions --------------------------------------------------------------------


#ifndef _MSC_VER
#include <gmpxx.h> // GNU arbit precision numbers

QTextStream& operator<<(QTextStream& ost, const std::string& str);

QTextStream& operator<<(QTextStream& ost, const mpz_class& c);

QDebug operator<<(QDebug debug, const mpz_class& c);

#endif

// legacy line readers, predating the readXXX/parseXXX template family below -
// kept for existing callers; readStringType() is their concept-based successor
bool getline(QTextStream& in, std::string& ret, const QString& prompt = "");

bool getline(QTextStream& in, QString& ret, const QString& prompt = "");

bool readString(QTextStream& in, QString& ret, const QString& prompt = "");

/*
 * converts a QLocale to the matching std::locale, for use with std::tm/
 * std::get_time parsing in readDateTimeType()/parseDateTimeType(). QLocale
 * and std::locale are unrelated locale systems: QLocale::c() maps straight
 * to std::locale::classic() with no OS lookup at all (the default-argument
 * fast path, and what every existing call already gets today). For any
 * other QLocale, std::locale(name) depends on that locale being installed
 * on the host OS and can throw std::runtime_error if it isn't - unlike
 * QLocale, whose data is bundled with Qt and never fails to construct. On
 * that failure we fall back to the classic locale and emit a warning
 * rather than letting the exception propagate, so a std::tm caller never
 * has to know or care that the fallback happened.
 */
inline std::locale toStdLocale(const QLocale& locale)
{
  if (locale == QLocale::c())
    return std::locale::classic();

  try {
    return std::locale(locale.name().toStdString());
  } catch (const std::runtime_error&) {
    qWarning() << "locale" << locale.name()
               << "not available on this system - falling back to the classic "
                  "locale for std::tm parsing";
    return std::locale::classic();
  }
}

/*
 * matches trimmed text (case-insensitively) against common true/false
 * tokens - "true"/"false", "1"/"0", "yes"/"no", "y"/"n", "t"/"f" - writing
 * the result to out and returning whether a match was found. Shared by
 * readBoolType() and parseBoolType() so neither has to duplicate the token
 * list; kept separate from both rather than having one call the other,
 * matching how every other read/parse pair in this file is an independent
 * (not delegating) implementation.
 */
inline bool matchBoolText(const QString& text, bool& out)
{
  const QString t = text.trimmed();
  if (t.compare("true", Qt::CaseInsensitive) == 0 || t == "1" ||
      t.compare("yes", Qt::CaseInsensitive) == 0 || t.compare("y", Qt::CaseInsensitive) == 0 ||
      t.compare("t", Qt::CaseInsensitive) == 0) {
    out = true;
    return true;
  }
  if (t.compare("false", Qt::CaseInsensitive) == 0 || t == "0" ||
      t.compare("no", Qt::CaseInsensitive) == 0 || t.compare("n", Qt::CaseInsensitive) == 0 ||
      t.compare("f", Qt::CaseInsensitive) == 0) {
    out = false;
    return true;
  }
  return false;
}

// ============================================================================
// readXXX functions
// ============================================================================

/*
 * reads a single character of any CharType from the stream. Qt has no
 * per-type to<Type>() conversion for characters the way it does for
 * integers/floats, so the line is read as a QString, trimmed, and the
 * first QChar is converted to T. Note: the char/char8_t branches go
 * through QChar::toLatin1(), so non-Latin-1 input is lossy for those two
 * types - use char16_t/char32_t/wchar_t if you need full Unicode.
 * Returns false if the (trimmed) line was empty.
 *
 * Example (char):
 *   char initial{}; // this could be any CharType
 *   if (readCharType(in, initial, "Enter your initial: "))
 *     out << "You entered: " << initial << Qt::endl;
 *   else
 *     out << "No character entered!" << Qt::endl;
 */
template <CharType T>
bool readCharType(QTextStream& in, T& ret, const QString& prompt = "")
{
#ifdef USING_QT6
  QTextStream out(stdout, QIODeviceBase::WriteOnly);
#else
  QTextStream out(stdout, QIODevice::WriteOnly);
#endif

  if (!prompt.isEmpty()) {
    out << prompt << Qt::flush;
  }
  QString line = in.readLine().trimmed();
  if (line.isEmpty())
    return false;
  QChar ch = line.at(0);
  if constexpr (std::same_as<T, char>)
    ret = ch.toLatin1();
  else if constexpr (std::same_as<T, wchar_t>)
    ret = static_cast<wchar_t>(ch.unicode());
  else if constexpr (std::same_as<T, char8_t>)
    ret = static_cast<char8_t>(ch.toLatin1());
  else if constexpr (std::same_as<T, char16_t>)
    ret = static_cast<char16_t>(ch.unicode());
  else if constexpr (std::same_as<T, char32_t>)
    ret = static_cast<char32_t>(ch.unicode());
  return true;
}

/*
 * reads a full line of text into a QString or std::string. Unlike
 * readCharType(), the whole (untrimmed) line is kept - only the trailing
 * newline consumed by QTextStream::readLine() is stripped. Returns false
 * only when the stream had nothing left to give at all (readLine() returns
 * a null QString); an empty line the user just pressed Enter on is a
 * valid, successful read, same as getline()'s isNull()-based check.
 *
 * Example (QString):
 *   QString name; // this could also be a std::string
 *   if (readStringType(in, name, "Enter your name: "))
 *     out << "You entered: " << name << Qt::endl;
 *   else
 *     out << "No input!" << Qt::endl;
 */
template <StringType T>
bool readStringType(QTextStream& in, T& ret, const QString& prompt = "")
{
#ifdef USING_QT6
  QTextStream out(stdout, QIODeviceBase::WriteOnly);
#else
  QTextStream out(stdout, QIODevice::WriteOnly);
#endif

  if (!prompt.isEmpty()) {
    out << prompt << Qt::flush;
  }
  QString line = in.readLine();
  if constexpr (std::same_as<T, QString>)
    ret = line;
  else
    if constexpr (std::same_as<T, std::string>)
      ret = line.toStdString();
  return !line.isNull();
}

/*
 * reads a single line and interprets it as a boolean via matchBoolText().
 * Unlike the numeric/date functions below, this is deliberately NOT
 * locale-aware: QLocale has no notion of localized true/false text (that's
 * a date/number-formatting concept, not something CLDR encodes), so adding
 * a locale parameter here would be a parameter that lies about what it
 * does. A blank line is NOT treated as false - only a recognized token
 * (see matchBoolText()) counts as a successful read.
 *
 * Example:
 *   bool isMarried{};
 *   if (readBoolType(in, isMarried, "Are you married (yes/no)? "))
 *     out << "You entered: " << (isMarried ? "yes" : "no") << Qt::endl;
 *   else
 *     out << "Please answer yes or no!" << Qt::endl;
 */
inline bool readBoolType(QTextStream& in, bool& ret, const QString& prompt = "")
{
#ifdef USING_QT6
  QTextStream out(stdout, QIODeviceBase::WriteOnly);
#else
  QTextStream out(stdout, QIODevice::WriteOnly);
#endif

  if (!prompt.isEmpty()) {
    out << prompt << Qt::flush;
  }
  QString line = in.readLine();
  return matchBoolText(line, ret);
}

// bool readInt(QTextStream& in, int& ret, const QString& prompt = "");

/*
 * replaces readInt(); works for short/int/long/long long (qint64) and their
 * unsigned counterparts, deducing T from ret. Each branch defers to the
 * matching QLocale::to<Type>() overload, so out-of-range input is still
 * rejected the same way it was for the original readInt(). locale defaults
 * to QLocale::c() (the classic "C" locale), which reproduces the exact
 * behaviour QString::to<Type>() always had - ASCII digits only, no grouping
 * separators. Pass e.g. QLocale(QLocale::English, QLocale::India) to accept
 * locale-formatted input such as "1,23,456".
 *
 * Example (int):
 *   int age{}; // this could be any integral type!
 *   if (readIntegerType(in, age, "Enter your age: "))
 *     out << "You entered: " << age << Qt::endl;
 *   else
 *     out << "Invalid integer!" << Qt::endl;
 *
 * Example (non-default locale - accepts "1,23,456" style grouping):
 *   int population{};
 *   QLocale inLocale(QLocale::English, QLocale::India);
 *   if (readIntegerType(in, population, "Enter the population: ", inLocale))
 *     out << "You entered: " << population << Qt::endl;
 *   else
 *     out << "Invalid integer!" << Qt::endl;
 */
template <IntegerType T>
bool readIntegerType(QTextStream& in, T& ret, const QString& prompt = "",
                      const QLocale& locale = QLocale::c())
{
#ifdef USING_QT6
  QTextStream out(stdout, QIODeviceBase::WriteOnly);
#else
  QTextStream out(stdout, QIODevice::WriteOnly);
#endif
  bool ok = false;
  if (!prompt.isEmpty()) {
    out << prompt << Qt::flush;
  }
  QString line = in.readLine();
  if constexpr (std::same_as<T, short>)
    ret = locale.toShort(line, &ok);
  else if constexpr (std::same_as<T, unsigned short>)
    ret = locale.toUShort(line, &ok);
  else if constexpr (std::same_as<T, int>)
    ret = locale.toInt(line, &ok);
  else if constexpr (std::same_as<T, unsigned int>)
    ret = locale.toUInt(line, &ok);
  else if constexpr (std::same_as<T, long>)
    ret = locale.toLong(line, &ok);
  else if constexpr (std::same_as<T, unsigned long>)
    ret = locale.toULong(line, &ok);
  else if constexpr (std::same_as<T, long long>)
    ret = locale.toLongLong(line, &ok);
  else if constexpr (std::same_as<T, unsigned long long>)
    ret = locale.toULongLong(line, &ok);
  return ok;
}

// bool readDouble(QTextStream& in, double& ret, const QString& prompt = "");

/*
 * replaces readDouble(); works for both float and double, deducing T from
 * ret. Each branch defers to the matching QLocale::to<Type>() overload, so
 * out-of-range/malformed input is still rejected the same way it was for
 * the original readDouble(). Same locale defaulting as readIntegerType():
 * QLocale::c() by default (matches the old QString::toDouble() behaviour -
 * '.' as the decimal point, no grouping), or pass a specific QLocale for
 * locale-formatted input (e.g. ',' as the decimal point in de_DE).
 *
 * Example (double):
 *   double price{}; // this could also be a float
 *   if (readFloatType(in, price, "Enter the price: "))
 *     out << "You entered: " << price << Qt::endl;
 *   else
 *     out << "Invalid number!" << Qt::endl;
 *
 * Example (non-default locale - accepts "19,99" as a German decimal comma):
 *   double preis{};
 *   QLocale deLocale(QLocale::German, QLocale::Germany);
 *   if (readFloatType(in, preis, "Preis eingeben: ", deLocale))
 *     out << "You entered: " << preis << Qt::endl;
 *   else
 *     out << "Invalid number!" << Qt::endl;
 */
template <FloatType T>
bool readFloatType(QTextStream& in, T& ret, const QString& prompt = "",
                    const QLocale& locale = QLocale::c())
{
#ifdef USING_QT6
  QTextStream out(stdout, QIODeviceBase::WriteOnly);
#else
  QTextStream out(stdout, QIODevice::WriteOnly);
#endif
  bool ok = false;

  if (!prompt.isEmpty()) {
    out << prompt << Qt::flush;
  }
  QString line = in.readLine();

  if constexpr (std::same_as<T, float>)
    ret = locale.toFloat(line, &ok);
  else if constexpr (std::same_as<T, double>)
    ret = locale.toDouble(line, &ok);

  return ok;
}

/*
 * reads a QDate, QTime, QDateTime, std::tm, or (C++23 compilers only - see
 * CHOCOLAF_HAVE_CHRONO_PARSE) std::chrono::year_month_day from the stream,
 * parsed using the given format string. Unlike readIntegerType()/
 * readFloatType(), format has no default - there's no single "natural"
 * date/time format, so the caller must always say how to interpret the
 * input.
 *
 * IMPORTANT: the format syntax depends on T. QDate/QTime/QDateTime use Qt
 * tokens (e.g. "dd-MM-yyyy", "HH:mm:ss"); std::tm and
 * std::chrono::year_month_day both use strftime-style tokens instead (e.g.
 * "%d-%m-%Y", "%H:%M:%S", via std::get_time()/std::chrono::parse()
 * respectively) - Qt tokens and strftime tokens are different
 * mini-languages and are not interchangeable.
 *
 * locale defaults to QLocale::c(), matching the previous behaviour exactly:
 * QDate::fromString()/QTime::fromString()/QDateTime::fromString() already
 * only ever accepted English/C-locale month and day names, which is what
 * QLocale::c().toDate()/toTime()/toDateTime() also do. Pass a different
 * QLocale to accept locale-specific month/day names (e.g. "MMM" matching
 * that locale's abbreviated month names instead of always "Jan"/"Feb"/...).
 * For T = std::tm or std::chrono::year_month_day there is no QLocale
 * involved at all - toStdLocale() bridges to the matching std::locale
 * instead (see its own comment for the fallback behaviour if that locale
 * isn't installed on the host OS).
 *
 * Example (QDate):
 *   QDate dob;
 *   if (readDateTimeType(in, dob, "dd-MM-yyyy", "Enter your date of birth: "))
 *     out << "You entered: " << dob.toString("dd-MMM-yyyy") << Qt::endl;
 *   else
 *     out << "Invalid date!" << Qt::endl;
 *
 * Example (std::tm):
 *   std::tm dobStl{};
 *   if (readDateTimeType(in, dobStl, "%d-%m-%Y", "Enter your date of birth: "))
 *     out << "You entered: " << std::put_time(&dobStl, "%d-%b-%Y") << std::endl;
 *   else
 *     out << "Invalid date!" << std::endl;
 *
 * Example (QDate, non-default locale - accepts French month names for "MMM"):
 *   QDate dobFr;
 *   QLocale frLocale(QLocale::French, QLocale::France);
 *   if (readDateTimeType(in, dobFr, "dd-MMM-yyyy", "Entrez votre date de naissance: ", frLocale))
 *     out << "You entered: " << dobFr.toString("dd-MMM-yyyy") << Qt::endl;
 *   else
 *     out << "Invalid date!" << Qt::endl;
 *
 * Example (std::tm, non-default locale - relies on the OS having "fr_FR"
 * installed; falls back to the classic locale via toStdLocale() otherwise):
 *   std::tm dobFrStl{};
 *   QLocale frLocale(QLocale::French, QLocale::France);
 *   if (readDateTimeType(in, dobFrStl, "%d-%b-%Y", "Entrez votre date de naissance: ", frLocale))
 *     out << "You entered: " << std::put_time(&dobFrStl, "%d-%b-%Y") << std::endl;
 *   else
 *     out << "Invalid date!" << std::endl;
 */
template <DateTimeType T>
bool readDateTimeType(QTextStream& in, T& ret, const QString& format, const QString& prompt = "",
                       const QLocale& locale = QLocale::c())
{
#ifdef USING_QT6
  QTextStream out(stdout, QIODeviceBase::WriteOnly);
#else
  QTextStream out(stdout, QIODevice::WriteOnly);
#endif

  if (!prompt.isEmpty()) {
    out << prompt << Qt::flush;
  }

  QString line = in.readLine().trimmed();

  if constexpr (std::same_as<T, std::tm>) {
    ret = std::tm{};
    std::istringstream iss(line.toStdString());
    iss.imbue(toStdLocale(locale));
    iss >> std::get_time(&ret, format.toStdString().c_str());
    return !iss.fail() && (iss >> std::ws).eof();
  }
  else if constexpr (std::same_as<T, QDate>) {
    ret = locale.toDate(line, format);
    return ret.isValid();
  }
  else if constexpr (std::same_as<T, QTime>) {
    ret = locale.toTime(line, format);
    return ret.isValid();
  }
  else if constexpr (std::same_as<T, QDateTime>) {
    ret = locale.toDateTime(line, format);
    return ret.isValid();
  }
#if CHOCOLAF_HAVE_CHRONO_PARSE
  else if constexpr (std::same_as<T, std::chrono::year_month_day>) {
    ret = std::chrono::year_month_day{};
    std::istringstream iss(line.toStdString());
    iss.imbue(toStdLocale(locale));
    iss >> std::chrono::parse(format.toStdString(), ret);
    return !iss.fail() && ret.ok() && (iss >> std::ws).eof();
  }
#endif
}

// ============================================================================
// parseXXX functions
// ============================================================================

/*
 * parses a QString or std::string as a boolean via matchBoolText() - see
 * readBoolType() for why this is deliberately not locale-aware.
 *
 * Example (QString -> bool):
 *   bool isMarried{};
 *   if (parseBoolType(QString("yes"), isMarried))
 *     out << "Parsed: " << (isMarried ? "yes" : "no") << Qt::endl;
 *   else
 *     out << "Invalid boolean!" << Qt::endl;
 */
template <StringType S>
bool parseBoolType(const S& fromString, bool& target)
{
  QString str;
  if constexpr (std::same_as<S, QString>)
    str = fromString;
  else if constexpr (std::same_as<S, std::string>)
    str = QString::fromStdString(fromString);

  return matchBoolText(str, target);
}

/*
 * parses an IntegerType out of a QString or std::string, with no prompting
 * or stream I/O involved - pure parsing. Same per-type QLocale::to<Type>()
 * dispatch (and therefore the same range checking and locale defaulting) as
 * readIntegerType().
 *
 * Example (QString -> int):
 *   int age{};
 *   if (parseIntegerType(QString("42"), age))
 *     out << "Parsed: " << age << Qt::endl;
 *   else
 *     out << "Invalid integer!" << Qt::endl;
 *
 * Example (non-default locale - accepts "1,23,456" style grouping):
 *   int population{};
 *   QLocale inLocale(QLocale::English, QLocale::India);
 *   if (parseIntegerType(QString("1,23,456"), population, inLocale))
 *     out << "Parsed: " << population << Qt::endl;
 *   else
 *     out << "Invalid integer!" << Qt::endl;
 */
template <StringType S, IntegerType T>
bool parseIntegerType(const S& fromString, T& target, const QLocale& locale = QLocale::c())
{
  bool ok = false;
  QString str;
  if constexpr (std::same_as<S, QString>)
    str = fromString;
  else if constexpr (std::same_as<S, std::string>)
    str = QString::fromStdString(fromString);

  if constexpr (std::same_as<T, short>)
    target = locale.toShort(str, &ok);
  else if constexpr (std::same_as<T, unsigned short>)
    target = locale.toUShort(str, &ok);
  else if constexpr (std::same_as<T, int>)
    target = locale.toInt(str, &ok);
  else if constexpr (std::same_as<T, unsigned int>)
    target = locale.toUInt(str, &ok);
  else if constexpr (std::same_as<T, long>)
    target = locale.toLong(str, &ok);
  else if constexpr (std::same_as<T, unsigned long>)
    target = locale.toULong(str, &ok);
  else if constexpr (std::same_as<T, long long>)
    target = locale.toLongLong(str, &ok);
  else if constexpr (std::same_as<T, unsigned long long>)
    target = locale.toULongLong(str, &ok);

  return ok;
}

/*
 * parses a FloatType (float/double) out of a QString or std::string. Same
 * locale defaulting as parseIntegerType()/readFloatType().
 *
 * Example (std::string -> double):
 *   double price{};
 *   if (parseFloatType(std::string("19.99"), price))
 *     out << "Parsed: " << price << Qt::endl;
 *   else
 *     out << "Invalid number!" << Qt::endl;
 *
 * Example (non-default locale - accepts "19,99" as a German decimal comma):
 *   double preis{};
 *   QLocale deLocale(QLocale::German, QLocale::Germany);
 *   if (parseFloatType(QString("19,99"), preis, deLocale))
 *     out << "Parsed: " << preis << Qt::endl;
 *   else
 *     out << "Invalid number!" << Qt::endl;
 */
template <StringType S, FloatType T>
bool parseFloatType(const S& fromString, T& target, const QLocale& locale = QLocale::c())
{
  bool ok = false;
  QString str;
  if constexpr (std::same_as<S, QString>)
    str = fromString;
  else if constexpr (std::same_as<S, std::string>)
    str = QString::fromStdString(fromString);

  if constexpr (std::same_as<T, float>)
    target = locale.toFloat(str, &ok);
  else if constexpr (std::same_as<T, double>)
    target = locale.toDouble(str, &ok);

  return ok;
}

/*
 * parses a DateTimeType (QDate/QTime/QDateTime/std::tm) out of a QString or
 * std::string, given a format string - same per-T dispatch, format-token
 * caveat (Qt tokens vs. strftime tokens), and locale handling (including the
 * std::tm -> std::locale bridge via toStdLocale()) as readDateTimeType().
 *
 * Example (QString -> QDate):
 *   QDate dob;
 *   if (parseDateTimeType(QString("23-09-2026"), dob, "dd-MM-yyyy"))
 *     out << "Parsed: " << dob.toString("dd-MMM-yyyy") << Qt::endl;
 *   else
 *     out << "Invalid date!" << Qt::endl;
 *
 * Example (non-default locale - accepts French month names for "MMM"):
 *   QDate dobFr;
 *   QLocale frLocale(QLocale::French, QLocale::France);
 *   if (parseDateTimeType(QString("23-sept.-2026"), dobFr, "dd-MMM-yyyy", frLocale))
 *     out << "Parsed: " << dobFr.toString("dd-MMM-yyyy") << Qt::endl;
 *   else
 *     out << "Invalid date!" << Qt::endl;
 */
template <StringType S, DateTimeType T>
bool parseDateTimeType(const S& fromString, T& target, const QString& format,
                        const QLocale& locale = QLocale::c())
{
  QString str;
  if constexpr (std::same_as<S, QString>)
    str = fromString;
  else if constexpr (std::same_as<S, std::string>)
    str = QString::fromStdString(fromString);

  if constexpr (std::same_as<T, std::tm>) {
    target = std::tm{};
    std::istringstream iss(str.toStdString());
    iss.imbue(toStdLocale(locale));
    iss >> std::get_time(&target, format.toStdString().c_str());
    return !iss.fail() && (iss >> std::ws).eof();
  }
  else if constexpr (std::same_as<T, QDate>) {
    target = locale.toDate(str, format);
    return target.isValid();
  }
  else if constexpr (std::same_as<T, QTime>) {
    target = locale.toTime(str, format);
    return target.isValid();
  }
  else if constexpr (std::same_as<T, QDateTime>) {
    target = locale.toDateTime(str, format);
    return target.isValid();
  }
#if CHOCOLAF_HAVE_CHRONO_PARSE
  else if constexpr (std::same_as<T, std::chrono::year_month_day>) {
    target = std::chrono::year_month_day{};
    std::istringstream iss(str.toStdString());
    iss.imbue(toStdLocale(locale));
    iss >> std::chrono::parse(format.toStdString(), target);
    return !iss.fail() && target.ok() && (iss >> std::ws).eof();
  }
#endif
}

bool fileExists(const QString& filepath);

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

    std::tm to_tm(const std::chrono::year_month_day& ymd)
    {
      std::tm tm_result{};
      tm_result.tm_year = static_cast<int>(ymd.year()) - 1900;   // tm_year = years since 1900
      tm_result.tm_mon = static_cast<unsigned>(ymd.month()) - 1; // tm_mon = [0, 11]
      tm_result.tm_mday = static_cast<unsigned>(ymd.day());

      // Other fields you might want to default to 0
      tm_result.tm_hour = 0;
      tm_result.tm_min = 0;
      tm_result.tm_sec = 0;
      tm_result.tm_isdst = -1; // Not known whether DST is in effect

      return tm_result;
    }

    std::string formatAsDate(const std::chrono::year_month_day& date)
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


//@formatter:on

#endif // __common_funcs_h__
