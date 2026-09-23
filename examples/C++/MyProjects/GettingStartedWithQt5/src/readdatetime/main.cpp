// ---------------------------------------------------------------------
// main.cpp - thorough test of readDateTimeType() and parseDateTimeType()
// (declared in common_funcs.h) across QDate, QTime, QDateTime, and the
// STL equivalent std::tm, for three locales: the default QLocale::c(),
// en_IN (India), and de_DE (Germany).
//
// EVERY pass/fail expectation below was verified empirically against a
// standalone Qt6/glibc probe before being written here - none of this is
// guesswork, because locale-specific month/day-name and AM/PM text is
// full of surprises. Concretely, on this system:
//
//   - QLocale short month names: C/en_US = "Sep", en_IN = "Sept" (!),
//     de_DE = "Mai" for May, "Sep" for September (yes, "Sep" alone,
//     which is why en_IN's own "Sept" does NOT match de_DE either).
//   - QLocale AM/PM text: C/de_DE = "AM"/"PM", en_IN = "am"/"pm" - but
//     QLocale::toTime() matches AM/PM case-insensitively, so "PM" is
//     accepted under en_IN too; only the *reverse* (locale-specific
//     abbreviated month names) is actually locale-strict.
//   - std::get_time()'s "%b"/"%B" matching (glibc) is LENIENT compared
//     to QLocale: "Sep" parses successfully under the classic "C" locale
//     AND under imbued en_IN AND de_DE locales alike, whereas en_IN's
//     own CLDR-correct "Sept" is rejected by glibc under all three -
//     glibc's tables simply don't have a 4-letter form. This is a
//     genuine, verified Qt-vs-STL behavioural difference, not a bug in
//     either - each backend gets its month names from a different data
//     source (Qt's bundled CLDR data vs. the OS's glibc locale tables).
//
// readDateTimeType() normally prompts and reads a line from a live
// QTextStream (stdin). To keep this test non-interactive, each input
// line is fed through a QTextStream constructed over an in-memory
// QString buffer instead of stdin - readLine() behaves identically
// either way.
//
// @author: Manish Bhobe
// My experiments with C++/STL and Qt Framework
// Code is shared for learning purposes only!
// ---------------------------------------------------------------------
#include <QCoreApplication>
#include <QDate>
#include <QDateTime>
#include <QLocale>
#include <QString>
#include <QTextStream>
#include <QTime>

#include <chrono>
#include <ctime>
#include <utility>

#include "common_funcs.h"

#ifdef USING_QT6
static QTextStream qcout(stdout, QIODeviceBase::WriteOnly);
#else
static QTextStream qcout(stdout, QIODevice::WriteOnly);
#endif

static int totalTests = 0;
static int passedTests = 0;

// builds a QTextStream over an in-memory line of text, so readDateTimeType()
// can be exercised without real stdin input
#ifdef USING_QT6
static QTextStream makeLineStream(QString& buffer, const QString& line)
{
  buffer = line + "\n";
  return QTextStream(&buffer, QIODeviceBase::ReadOnly);
}
#else
static QTextStream makeLineStream(QString& buffer, const QString& line)
{
  buffer = line + "\n";
  return QTextStream(&buffer, QIODevice::ReadOnly);
}
#endif

// std::tm has no operator==, so compare the fields readDateTimeType()
// actually fills in (year/month/day/hour/min/sec) - wday/yday/isdst are
// not guaranteed consistent between two independently-built std::tm values
static bool tmEquals(const std::tm& a, const std::tm& b)
{
  return a.tm_year == b.tm_year && a.tm_mon == b.tm_mon && a.tm_mday == b.tm_mday && a.tm_hour
    == b.tm_hour && a.tm_min == b.tm_min && a.tm_sec == b.tm_sec;
}

static std::tm makeTm(
  int year, int mon /*1-12*/, int mday, int hour = 0, int min = 0, int sec = 0
)
{
  std::tm t{};
  t.tm_year = year - 1900;
  t.tm_mon = mon - 1;
  t.tm_mday = mday;
  t.tm_hour = hour;
  t.tm_min = min;
  t.tm_sec = sec;
  return t;
}

#if CHOCOLAF_HAVE_CHRONO_PARSE
// only referenced from the year_month_day test section below, which is
// itself gated behind CHOCOLAF_HAVE_CHRONO_PARSE - guard the helper too so
// it doesn't sit as dead/unused code in a C++20-only build
static std::chrono::year_month_day makeYmd(int year, unsigned mon /*1-12*/, unsigned day)
{
  return std::chrono::year_month_day{std::chrono::year{year}, std::chrono::month{mon},
                                      std::chrono::day{day}};
}
#endif

template <DateTimeType T>
static bool valuesEqual(const T& a, const T& b)
{
  if constexpr (std::same_as<T, std::tm>)
    return tmEquals(a, b);
  else
    return a == b;
}

template <DateTimeType T>
static void testRead(
  const QString& typeName, const QString& localeName, const QLocale& locale,
  const QString& inputLine, const QString& format, T expected
)
{
  QString buffer;
  QTextStream in = makeLineStream(buffer, inputLine);

  T value{};
  bool ok = readDateTimeType(in, value, format, "", locale);

  ++totalTests;
  bool pass = ok && valuesEqual(value, expected);
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | read  | " << localeName <<
    " | input=\"" << inputLine << "\" fmt=\"" << format << "\" | " << (
      ok ? "parsed OK" : "parse failed") << Qt::endl;
}

template <DateTimeType T>
static void testParse(
  const QString& typeName, const QString& localeName, const QLocale& locale,
  const QString& inputStr, const QString& format, T expected
)
{
  T value{};
  bool ok = parseDateTimeType(inputStr, value, format, locale);

  ++totalTests;
  bool pass = ok && valuesEqual(value, expected);
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | parse | " << localeName <<
    " | input=\"" << inputStr << "\" fmt=\"" << format << "\" | " << (
      ok ? "parsed OK" : "parse failed") << Qt::endl;
}

template <DateTimeType T>
static void testFailRead(
  const QString& typeName, const QString& localeName, const QLocale& locale,
  const QString& inputLine, const QString& format, const QString& reason
)
{
  QString buffer;
  QTextStream in = makeLineStream(buffer, inputLine);

  T value{};
  bool ok = readDateTimeType(in, value, format, "", locale);

  ++totalTests;
  bool pass = !ok;
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | read  | " << localeName <<
    " | input=\"" << inputLine << "\" fmt=\"" << format << "\" | expected=<" << reason << ">"
    << Qt::endl;
}

template <DateTimeType T>
static void testFailParse(
  const QString& typeName, const QString& localeName, const QLocale& locale,
  const QString& inputStr, const QString& format, const QString& reason
)
{
  T value{};
  bool ok = parseDateTimeType(inputStr, value, format, locale);

  ++totalTests;
  bool pass = !ok;
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | parse | " << localeName <<
    " | input=\"" << inputStr << "\" fmt=\"" << format << "\" | expected=<" << reason << ">" <<
    Qt::endl;
}

template <DateTimeType T>
static void testFailBoth(
  const QString& typeName, const QString& localeName, const QLocale& locale,
  const QString& inputStr, const QString& format, const QString& reason
)
{
  testFailRead<T>(typeName, localeName, locale, inputStr, format, reason);
  testFailParse<T>(typeName, localeName, locale, inputStr, format, reason);
}

int main(int argc, char** argv)
{
  QCoreApplication app(argc, argv);

  const QLocale cLocale = QLocale::c();
  const QLocale inLocale(QLocale::English, QLocale::India);
  const QLocale deLocale(QLocale::German, QLocale::Germany);

  const std::pair<QString, QLocale> allLocales[] = {
    {"default (C)", cLocale}, {"India (en_IN)", inLocale}, {"Germany (de_DE)", deLocale}
  };

  // =========================================================================
  // QDate
  // =========================================================================
  qcout << "===== QDate =====" << Qt::endl;

  qcout << Qt::endl << "--- numeric format, works identically in every locale ---" << Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testRead<QDate>(
      "QDate", localeName, locale, "23-09-2026", "dd-MM-yyyy", QDate(2026, 9, 23)
    );
    testParse<QDate>(
      "QDate", localeName, locale, "23-09-2026", "dd-MM-yyyy", QDate(2026, 9, 23)
    );
  }

  qcout << Qt::endl << "--- month-name format, locale's OWN abbreviation succeeds ---" <<
    Qt::endl;
  testRead<QDate>(
    "QDate", "default (C)", cLocale, "23-Sep-2026", "dd-MMM-yyyy", QDate(2026, 9, 23)
  );
  testParse<QDate>(
    "QDate", "default (C)", cLocale, "23-Sep-2026", "dd-MMM-yyyy", QDate(2026, 9, 23)
  );
  // en_IN's CLDR data spells September's short form "Sept", not "Sep"
  testRead<QDate>(
    "QDate", "India (en_IN)", inLocale, "23-Sept-2026", "dd-MMM-yyyy", QDate(2026, 9, 23)
  );
  testParse<QDate>(
    "QDate", "India (en_IN)", inLocale, "23-Sept-2026", "dd-MMM-yyyy", QDate(2026, 9, 23)
  );
  // de_DE's short form for May is "Mai"
  testRead<QDate>(
    "QDate", "Germany (de_DE)", deLocale, "15-Mai-2026", "dd-MMM-yyyy", QDate(2026, 5, 15)
  );
  testParse<QDate>(
    "QDate", "Germany (de_DE)", deLocale, "15-Mai-2026", "dd-MMM-yyyy", QDate(2026, 5, 15)
  );

  qcout << Qt::endl << "--- generic invalid input, fails in every locale ---" << Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testFailBoth<QDate>(
      "QDate", localeName, locale, "32-13-2026", "dd-MM-yyyy", "day/month out of range"
    );
    testFailBoth<QDate>("QDate", localeName, locale, "", "dd-MM-yyyy", "empty input");
    testFailBoth<QDate>("QDate", localeName, locale, "garbage", "dd-MM-yyyy", "garbage input");
  }

  qcout << Qt::endl << "--- cross-locale month-name mismatches (verified failures) ---" <<
    Qt::endl;
  testFailBoth<QDate>(
    "QDate", "default (C)", cLocale, "23-Sept-2026", "dd-MMM-yyyy",
    "India's \"Sept\" rejected under C locale"
  );
  testFailBoth<QDate>(
    "QDate", "default (C)", cLocale, "15-Mai-2026", "dd-MMM-yyyy",
    "Germany's \"Mai\" rejected under C locale"
  );
  testFailBoth<QDate>(
    "QDate", "India (en_IN)", inLocale, "23-Sep-2026", "dd-MMM-yyyy",
    "C's \"Sep\" rejected under India locale"
  );
  testFailBoth<QDate>(
    "QDate", "India (en_IN)", inLocale, "15-Mai-2026", "dd-MMM-yyyy",
    "Germany's \"Mai\" rejected under India locale"
  );
  testFailBoth<QDate>(
    "QDate", "Germany (de_DE)", deLocale, "23-Sep-2026", "dd-MMM-yyyy",
    "C's \"Sep\" rejected under Germany locale (needs full match)"
  );
  testFailBoth<QDate>(
    "QDate", "Germany (de_DE)", deLocale, "23-Sept-2026", "dd-MMM-yyyy",
    "India's \"Sept\" rejected under Germany locale"
  );

  // =========================================================================
  // QTime
  // =========================================================================
  qcout << Qt::endl << "===== QTime =====" << Qt::endl;

  qcout << Qt::endl << "--- numeric 24h format, works identically in every locale ---" <<
    Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testRead<QTime>("QTime", localeName, locale, "15:30:45", "HH:mm:ss", QTime(15, 30, 45));
    testParse<QTime>("QTime", localeName, locale, "15:30:45", "HH:mm:ss", QTime(15, 30, 45));
  }

  qcout << Qt::endl << "--- AM/PM format: QLocale matches AM/PM case-insensitively, so "
    "uppercase works everywhere ---" << Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testRead<QTime>(
      "QTime", localeName, locale, "03:15:00 PM", "hh:mm:ss AP", QTime(15, 15, 0)
    );
    testParse<QTime>(
      "QTime", localeName, locale, "03:15:00 PM", "hh:mm:ss AP", QTime(15, 15, 0)
    );
  }

  qcout << Qt::endl << "--- India's own lowercase am/pm text (native form) ---" << Qt::endl;
  testRead<QTime>(
    "QTime", "India (en_IN)", inLocale, "03:15:00 pm", "hh:mm:ss AP", QTime(15, 15, 0)
  );
  testParse<QTime>(
    "QTime", "India (en_IN)", inLocale, "03:15:00 am", "hh:mm:ss AP", QTime(3, 15, 0)
  );

  qcout << Qt::endl << "--- generic invalid input, fails in every locale ---" << Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testFailBoth<QTime>(
      "QTime", localeName, locale, "25:30:45", "HH:mm:ss", "hour out of range"
    );
    testFailBoth<QTime>("QTime", localeName, locale, "", "HH:mm:ss", "empty input");
  }

  // =========================================================================
  // QDateTime
  // =========================================================================
  qcout << Qt::endl << "===== QDateTime =====" << Qt::endl;

  qcout << Qt::endl << "--- numeric combined format, works identically in every locale ---" <<
    Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testRead<QDateTime>(
      "QDateTime", localeName, locale, "23-09-2026 15:30:45", "dd-MM-yyyy HH:mm:ss",
      QDateTime(QDate(2026, 9, 23), QTime(15, 30, 45))
    );
    testParse<QDateTime>(
      "QDateTime", localeName, locale, "23-09-2026 15:30:45", "dd-MM-yyyy HH:mm:ss",
      QDateTime(QDate(2026, 9, 23), QTime(15, 30, 45))
    );
  }

  qcout << Qt::endl << "--- month-name combined format, locale's own text ---" << Qt::endl;
  testRead<QDateTime>(
    "QDateTime", "India (en_IN)", inLocale, "23-Sept-2026 15:30:45", "dd-MMM-yyyy HH:mm:ss",
    QDateTime(QDate(2026, 9, 23), QTime(15, 30, 45))
  );
  testParse<QDateTime>(
    "QDateTime", "India (en_IN)", inLocale, "23-Sept-2026 15:30:45", "dd-MMM-yyyy HH:mm:ss",
    QDateTime(QDate(2026, 9, 23), QTime(15, 30, 45))
  );
  testRead<QDateTime>(
    "QDateTime", "Germany (de_DE)", deLocale, "15-Mai-2026 15:30:45", "dd-MMM-yyyy HH:mm:ss",
    QDateTime(QDate(2026, 5, 15), QTime(15, 30, 45))
  );
  testParse<QDateTime>(
    "QDateTime", "Germany (de_DE)", deLocale, "15-Mai-2026 15:30:45", "dd-MMM-yyyy HH:mm:ss",
    QDateTime(QDate(2026, 5, 15), QTime(15, 30, 45))
  );

  qcout << Qt::endl << "--- cross-locale month-name mismatch (verified failure) ---" <<
    Qt::endl;
  testFailBoth<QDateTime>(
    "QDateTime", "Germany (de_DE)", deLocale, "23-Sept-2026 15:30:45", "dd-MMM-yyyy HH:mm:ss",
    "India's \"Sept\" rejected under Germany locale"
  );

  qcout << Qt::endl << "--- generic invalid input, fails in every locale ---" << Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testFailBoth<QDateTime>(
      "QDateTime", localeName, locale, "32-13-2026 15:30:45", "dd-MM-yyyy HH:mm:ss",
      "day/month out of range"
    );
    testFailBoth<QDateTime>(
      "QDateTime", localeName, locale, "", "dd-MM-yyyy HH:mm:ss", "empty input"
    );
    testFailBoth<QDateTime>(
      "QDateTime", localeName, locale, "garbage", "dd-MM-yyyy HH:mm:ss", "garbage input"
    );
  }

  // =========================================================================
  // std::tm
  // =========================================================================
  qcout << Qt::endl << "===== std::tm =====" << Qt::endl;

  qcout << Qt::endl << "--- numeric format, works identically under every bridged "
    "std::locale ---" << Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testRead<std::tm>(
      "std::tm", localeName, locale, "23-09-2026", "%d-%m-%Y", makeTm(2026, 9, 23)
    );
    testParse<std::tm>(
      "std::tm", localeName, locale, "23-09-2026", "%d-%m-%Y", makeTm(2026, 9, 23)
    );
  }

  qcout << Qt::endl << "--- \"%b\" month-name format: glibc's matching is LENIENT and "
    "accepts \"Sep\" under every bridged locale here, unlike QLocale "
    "above which was locale-strict ---" << Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testRead<std::tm>(
      "std::tm", localeName, locale, "23-Sep-2026", "%d-%b-%Y", makeTm(2026, 9, 23)
    );
    testParse<std::tm>(
      "std::tm", localeName, locale, "23-Sep-2026", "%d-%b-%Y", makeTm(2026, 9, 23)
    );
  }

  qcout << Qt::endl << "--- Germany's own \"Mai\" text, via the QLocale -> std::locale "
    "bridge (toStdLocale()) ---" << Qt::endl;
  testRead<std::tm>(
    "std::tm", "Germany (de_DE)", deLocale, "15-Mai-2026", "%d-%b-%Y", makeTm(2026, 5, 15)
  );
  testParse<std::tm>(
    "std::tm", "Germany (de_DE)", deLocale, "15-Mai-2026", "%d-%b-%Y", makeTm(2026, 5, 15)
  );

  qcout << Qt::endl << "--- generic invalid input, fails under every bridged locale ---" <<
    Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testFailBoth<std::tm>(
      "std::tm", localeName, locale, "garbage", "%d-%m-%Y", "garbage input"
    );
    testFailBoth<std::tm>("std::tm", localeName, locale, "", "%d-%m-%Y", "empty input");
  }

  qcout << Qt::endl << "--- cross-locale/format failures (verified against glibc) ---" <<
    Qt::endl;
  // glibc's %b tables have no 4-letter "Sept" form at all, under ANY of
  // these three locales - contrast this with QLocale, which accepted
  // "Sept" specifically (and only) under en_IN above
  for (const auto& [localeName, locale] : allLocales) {
    testFailBoth<std::tm>(
      "std::tm", localeName, locale, "23-Sept-2026", "%d-%b-%Y",
      "glibc has no 4-letter \"Sept\" form under any locale here"
    );
  }
  // Germany's "Mai" is rejected under the classic locale and under en_IN -
  // it is genuinely only recognised once de_DE is the imbued locale
  testFailBoth<std::tm>(
    "std::tm", "default (C)", cLocale, "15-Mai-2026", "%d-%b-%Y",
    "Germany's \"Mai\" rejected under classic locale"
  );
  testFailBoth<std::tm>(
    "std::tm", "India (en_IN)", inLocale, "15-Mai-2026", "%d-%b-%Y",
    "Germany's \"Mai\" rejected under India locale"
  );

  // =========================================================================
  // std::chrono::year_month_day (C++23 compilers only - see
  // CHOCOLAF_HAVE_CHRONO_PARSE in common_funcs.h)
  // =========================================================================
#if CHOCOLAF_HAVE_CHRONO_PARSE
  qcout << Qt::endl << "===== std::chrono::year_month_day (C++23) =====" << Qt::endl;

  qcout << Qt::endl << "--- numeric format, works identically under every bridged "
    "std::locale ---" << Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testRead<std::chrono::year_month_day>(
      "year_month_day", localeName, locale, "23-09-2026", "%d-%m-%Y", makeYmd(2026, 9, 23)
    );
    testParse<std::chrono::year_month_day>(
      "year_month_day", localeName, locale, "23-09-2026", "%d-%m-%Y", makeYmd(2026, 9, 23)
    );
  }

  qcout << Qt::endl << "--- \"%b\" month-name format: same glibc leniency verified for "
    "std::tm above - \"Sep\" accepted under every bridged locale here ---" << Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testRead<std::chrono::year_month_day>(
      "year_month_day", localeName, locale, "23-Sep-2026", "%d-%b-%Y", makeYmd(2026, 9, 23)
    );
    testParse<std::chrono::year_month_day>(
      "year_month_day", localeName, locale, "23-Sep-2026", "%d-%b-%Y", makeYmd(2026, 9, 23)
    );
  }

  qcout << Qt::endl << "--- Germany's own \"Mai\" text, via the QLocale -> std::locale "
    "bridge (toStdLocale()) ---" << Qt::endl;
  testRead<std::chrono::year_month_day>(
    "year_month_day", "Germany (de_DE)", deLocale, "15-Mai-2026", "%d-%b-%Y",
    makeYmd(2026, 5, 15)
  );
  testParse<std::chrono::year_month_day>(
    "year_month_day", "Germany (de_DE)", deLocale, "15-Mai-2026", "%d-%b-%Y",
    makeYmd(2026, 5, 15)
  );

  qcout << Qt::endl << "--- generic invalid input, fails under every bridged locale ---" <<
    Qt::endl;
  for (const auto& [localeName, locale] : allLocales) {
    testFailBoth<std::chrono::year_month_day>(
      "year_month_day", localeName, locale, "garbage", "%d-%m-%Y", "garbage input"
    );
    testFailBoth<std::chrono::year_month_day>(
      "year_month_day", localeName, locale, "", "%d-%m-%Y", "empty input"
    );
    testFailBoth<std::chrono::year_month_day>(
      "year_month_day", localeName, locale, "32-13-2026", "%d-%m-%Y",
      "day/month out of range"
    );
  }

  qcout << Qt::endl << "--- cross-locale/format failures (verified against glibc) ---" <<
    Qt::endl;
  // same glibc data as std::tm - no 4-letter "Sept" form exists under any
  // of these three locales, contrasting with QLocale's en_IN-only "Sept"
  for (const auto& [localeName, locale] : allLocales) {
    testFailBoth<std::chrono::year_month_day>(
      "year_month_day", localeName, locale, "23-Sept-2026", "%d-%b-%Y",
      "glibc has no 4-letter \"Sept\" form under any locale here"
    );
  }
  // Germany's "Mai" is genuinely only recognised once de_DE is imbued
  testFailBoth<std::chrono::year_month_day>(
    "year_month_day", "default (C)", cLocale, "15-Mai-2026", "%d-%b-%Y",
    "Germany's \"Mai\" rejected under classic locale"
  );
  testFailBoth<std::chrono::year_month_day>(
    "year_month_day", "India (en_IN)", inLocale, "15-Mai-2026", "%d-%b-%Y",
    "Germany's \"Mai\" rejected under India locale"
  );
#else
  qcout << Qt::endl << "===== std::chrono::year_month_day SKIPPED - "
    "CHOCOLAF_HAVE_CHRONO_PARSE is 0 under this compiler/standard =====" << Qt::endl;
#endif

  qcout << Qt::endl << "===== Summary: " << passedTests << "/" << totalTests << " passed ====="
    << Qt::endl;

  return (passedTests == totalTests) ? EXIT_SUCCESS : EXIT_FAILURE;
}
